"""
Unit tests for the Enhancement Three validation and access-control layer.

These tests need no MongoDB server: a small in-memory FakeCollection records every call,
so each test can also prove that rejected input never reached the database.

Run from the project folder:   python -m unittest discover -s tests -v
"""
import os
import sys
import unittest
from unittest import mock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import animal_shelter
from animal_shelter import AnimalShelter, DatabaseError, ValidationError
from pymongo.errors import PyMongoError

VALID_ANIMAL = {
    "animal_id": "A000001",
    "animal_type": "Dog",
    "breed": "Labrador Retriever Mix",
    "outcome_type": "Adoption",
    "sex_upon_outcome": "Spayed Female",
    "name": "Rex",
    "age_upon_outcome_in_weeks": 52.5,
}


class FakeCollection:
    """Stands in for a pymongo collection and records the calls it receives."""

    def __init__(self, error=None):
        self.calls = []
        self.error = error

    def _record(self, name, *args):
        if self.error:
            raise self.error
        self.calls.append((name,) + args)

    def find(self, query):
        self._record("find", query)
        return iter([{"animal_id": "A000001"}])

    def insert_one(self, doc):
        self._record("insert_one", doc)
        return mock.Mock(acknowledged=True)

    def update_many(self, query, update):
        self._record("update_many", query, update)
        return mock.Mock(modified_count=1)

    def delete_many(self, query):
        self._record("delete_many", query)
        return mock.Mock(deleted_count=1)


class ReadValidationTests(unittest.TestCase):
    def setUp(self):
        self.col = FakeCollection()
        self.db = AnimalShelter(collection=self.col)

    def test_valid_queries_reach_the_database(self):
        self.assertEqual(self.db.read({}), [{"animal_id": "A000001"}])
        self.db.read({"breed": "Labrador Retriever Mix"})
        self.db.read({"breed": {"$in": ["Labrador Retriever Mix", "Chesapeake Bay Retriever"]}})
        self.db.read({"$or": [{"animal_type": "Dog"}, {"animal_type": "Cat"}]})
        self.db.read({"age_upon_outcome_in_weeks": {"$gte": 26, "$lte": 156}})
        self.assertEqual(len(self.col.calls), 5)

    def test_where_operator_is_rejected(self):
        # classic server-side JavaScript injection
        with self.assertRaises(ValidationError):
            self.db.read({"$where": "sleep(5000)"})
        self.assertEqual(self.col.calls, [])

    def test_operator_injection_is_rejected(self):
        # {"$ne": None} is the usual authentication-bypass / match-everything trick
        with self.assertRaises(ValidationError):
            self.db.read({"breed": {"$ne": None}})
        with self.assertRaises(ValidationError):
            self.db.read({"breed": {"$regex": ".*"}})
        with self.assertRaises(ValidationError):
            self.db.read({"breed": {"$where": "1 == 1"}})
        self.assertEqual(self.col.calls, [])

    def test_unknown_field_and_wrong_types_are_rejected(self):
        for bad in ({"password": "x"}, {"animal_id": 123}, {"age_upon_outcome_in_weeks": "52"},
                    {"age_upon_outcome_in_weeks": True}, {"breed": "x" * 101}, "breed=Dog", None):
            with self.subTest(bad=bad):
                with self.assertRaises(ValidationError):
                    self.db.read(bad)
        self.assertEqual(self.col.calls, [])

    def test_list_and_nesting_limits(self):
        with self.assertRaises(ValidationError):
            self.db.read({"breed": {"$in": []}})
        with self.assertRaises(ValidationError):
            self.db.read({"breed": {"$in": ["a"] * 101}})
        deep = {"animal_type": "Dog"}
        for _ in range(5):
            deep = {"$and": [deep]}
        with self.assertRaises(ValidationError):
            self.db.read(deep)


class CreateTests(unittest.TestCase):
    def setUp(self):
        self.col = FakeCollection()
        self.db = AnimalShelter(collection=self.col)

    def test_valid_document_is_inserted(self):
        self.assertTrue(self.db.create(dict(VALID_ANIMAL)))
        self.assertEqual(self.col.calls[0][0], "insert_one")

    def test_missing_required_field(self):
        doc = dict(VALID_ANIMAL)
        del doc["breed"]
        with self.assertRaises(ValidationError):
            self.db.create(doc)

    def test_unknown_or_operator_keys_rejected(self):
        for extra in ({"admin": True}, {"$set": {"x": 1}}, {"a.b": 1}):
            with self.subTest(extra=extra):
                with self.assertRaises(ValidationError):
                    self.db.create({**VALID_ANIMAL, **extra})

    def test_wrong_type_rejected(self):
        with self.assertRaises(ValidationError):
            self.db.create({**VALID_ANIMAL, "age_upon_outcome_in_weeks": "old"})
        self.assertEqual(self.col.calls, [])


class UpdateDeleteGuardTests(unittest.TestCase):
    def setUp(self):
        self.col = FakeCollection()
        self.db = AnimalShelter(collection=self.col)

    def test_update_with_filter(self):
        self.assertEqual(self.db.update({"animal_id": "A000001"}, {"outcome_type": "Transfer"}), 1)

    def test_empty_filter_update_and_delete_refused(self):
        with self.assertRaises(ValidationError):
            self.db.update({}, {"outcome_type": "Transfer"})
        with self.assertRaises(ValidationError):
            self.db.delete({})
        self.assertEqual(self.col.calls, [])

    def test_allow_all_is_an_explicit_override(self):
        self.assertEqual(self.db.delete({}, allow_all=True), 1)
        self.assertEqual(self.db.update({}, {"outcome_type": "Transfer"}, allow_all=True), 1)

    def test_identity_fields_cannot_be_updated(self):
        with self.assertRaises(ValidationError):
            self.db.update({"animal_id": "A000001"}, {"animal_id": "A999999"})

    def test_operator_in_update_data_rejected(self):
        with self.assertRaises(ValidationError):
            self.db.update({"animal_id": "A000001"}, {"$unset": {"name": 1}})
        self.assertEqual(self.col.calls, [])

    def test_delete_with_injection_rejected(self):
        with self.assertRaises(ValidationError):
            self.db.delete({"animal_id": {"$ne": ""}})
        self.assertEqual(self.col.calls, [])


    def test_writes_allow_exact_match_only(self):
        # $gt / $ne / $nin can match nearly every record, so they are read-only operators
        for bad in ({"animal_id": {"$gt": ""}}, {"animal_id": {"$nin": ["x"]}},
                    {"$or": [{"animal_id": {"$ne": ""}}]}):
            with self.subTest(bad=bad):
                with self.assertRaises(ValidationError):
                    self.db.delete(bad)
                with self.assertRaises(ValidationError):
                    self.db.update(bad, {"outcome_type": "Transfer"})
        self.assertEqual(self.db.delete({"animal_id": {"$in": ["A1", "A2"]}}), 1)
        self.assertEqual(self.col.calls, [("delete_many", {"animal_id": {"$in": ["A1", "A2"]}})])


class ReadOnlyTests(unittest.TestCase):
    def test_writes_blocked_reads_allowed(self):
        col = FakeCollection()
        db = AnimalShelter(read_only=True, collection=col)
        with self.assertRaises(PermissionError):
            db.create(dict(VALID_ANIMAL))
        with self.assertRaises(PermissionError):
            db.update({"animal_id": "A000001"}, {"outcome_type": "Transfer"})
        with self.assertRaises(PermissionError):
            db.delete({"animal_id": "A000001"})
        self.assertEqual(col.calls, [])
        self.assertEqual(len(db.read({})), 1)


class HonestErrorTests(unittest.TestCase):
    def test_database_errors_are_raised_not_swallowed(self):
        db = AnimalShelter(collection=FakeCollection(error=PyMongoError("boom")))
        with self.assertRaises(DatabaseError):
            db.read({})
        with self.assertRaises(DatabaseError):
            db.create(dict(VALID_ANIMAL))
        with self.assertRaises(DatabaseError):
            db.update({"animal_id": "A000001"}, {"outcome_type": "Transfer"})
        with self.assertRaises(DatabaseError):
            db.delete({"animal_id": "A000001"})


class ConnectionSettingsTests(unittest.TestCase):
    ENV = {"MONGO_DATABASE": "aac", "MONGO_COLLECTION": "animals"}

    def _build(self, env, **kwargs):
        with mock.patch.dict(os.environ, env, clear=True), \
             mock.patch.object(animal_shelter, "load_dotenv"):
            return AnimalShelter(**kwargs)

    def test_missing_credentials_fail_fast(self):
        with self.assertRaises(ValueError):
            self._build(self.ENV)

    def test_missing_database_name_fails_fast(self):
        with self.assertRaises(ValueError):
            self._build({"MONGO_USER": "u", "MONGO_PASSWORD": "p"})

    def test_bad_port_rejected(self):
        with self.assertRaises(ValueError):
            self._build({**self.ENV, "MONGO_PORT": "27017/evil"}, username="u", password="p")

    def test_credentials_are_escaped_and_connection_is_verified(self):
        with mock.patch.object(animal_shelter, "MongoClient") as client_cls:
            self._build(self.ENV, username="user", password="p@ss:/w?rd")
        uri = client_cls.call_args[0][0]
        self.assertIn("user:p%40ss%3A%2Fw%3Frd@", uri)       # special characters cannot alter the URI
        self.assertIn("authSource=aac", uri)
        client_cls.return_value.admin.command.assert_called_with("ping")

    def test_connection_failure_does_not_leak_password(self):
        with mock.patch.object(animal_shelter, "MongoClient") as client_cls:
            client_cls.return_value.admin.command.side_effect = PyMongoError("auth failed")
            with self.assertRaises(DatabaseError) as ctx:
                self._build(self.ENV, username="user", password="SuperSecret1")
        self.assertNotIn("SuperSecret1", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
