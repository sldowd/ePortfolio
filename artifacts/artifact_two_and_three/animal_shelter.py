"""
Animal Shelter CRUD Module
Provides Create, Read, Update, and Delete operations for the MongoDB shelter database.

Enhancement Three (Databases): a validation and access-control layer.
  - Every query and document is checked against an allow-list before it reaches MongoDB,
    which blocks NoSQL injection (for example {"$where": ...} or {"breed": {"$ne": null}}).
  - Update and delete refuse an empty filter, so one bad call cannot wipe the collection.
  - Failures raise clear exceptions instead of being printed and silently turned into [] / 0 / False.
  - Credentials are URL-escaped, connection settings are validated, and the connection is
    verified at startup (MongoClient connects lazily, so the original try/except never fired).
  - read_only mode blocks writes in the application, backing up a read-only database user.
"""

import logging
import os
from urllib.parse import quote_plus

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import PyMongoError

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------
class ValidationError(ValueError):
    """A query or document failed validation and was never sent to the database."""


class DatabaseError(Exception):
    """A connection or database operation failed."""


# ---------------------------------------------------------------------------
# Validation rules
# ---------------------------------------------------------------------------
NUMBER = (int, float)

# Allow-list of field names and the value types each may hold. Mirrors the AAC dataset.
# Anything not listed here is rejected, including MongoDB operators used as field names.
FIELD_TYPES = {
    "rec_num": (int,),
    "age_upon_outcome": (str,),
    "animal_id": (str,),
    "animal_type": (str,),
    "breed": (str,),
    "color": (str,),
    "date_of_birth": (str,),
    "datetime": (str,),
    "monthyear": (str,),
    "name": (str, int),            # a few records in the dataset store a numeric name
    "outcome_subtype": (str,),
    "outcome_type": (str,),
    "sex_upon_outcome": (str,),
    "location_lat": NUMBER,
    "location_long": NUMBER,
    "age_upon_outcome_in_weeks": NUMBER,
}

REQUIRED_ON_CREATE = ("animal_id", "animal_type", "breed", "outcome_type", "sex_upon_outcome")
IMMUTABLE_FIELDS = ("animal_id", "rec_num")   # identity fields cannot be changed by update()

# Only these query operators are permitted. $where, $regex, $expr, $function and the
# rest are deliberately absent, because they can run attacker-controlled logic.
COMPARISON_OPERATORS = {"$eq", "$ne", "$gt", "$gte", "$lt", "$lte"}
LIST_OPERATORS = {"$in", "$nin"}
LOGICAL_OPERATORS = {"$and", "$or"}
# update() and delete() may only target exact matches. Operators such as $ne or $gt can match
# nearly every record, which would get around the empty-filter guard.
WRITE_OPERATORS = {"$eq", "$in"}

MAX_STRING_LENGTH = 100
MAX_LIST_LENGTH = 100
MAX_QUERY_DEPTH = 3


def _type_names(types):
    return "/".join(t.__name__ for t in types)


def _check_value(field, value):
    """Validate one value against the declared type for its field."""
    types = FIELD_TYPES[field]
    # bool is a subclass of int in Python, so reject it explicitly for numeric fields
    if isinstance(value, bool) or not isinstance(value, types):
        raise ValidationError(f"Field '{field}' expects {_type_names(types)}, got {type(value).__name__}")
    if isinstance(value, str) and len(value) > MAX_STRING_LENGTH:
        raise ValidationError(f"Field '{field}' exceeds {MAX_STRING_LENGTH} characters")


def _check_field_condition(field, condition, writing=False):
    """Validate the right-hand side of a query field: a plain value or an operator dict."""
    if not isinstance(condition, dict):
        _check_value(field, condition)
        return
    if not condition:
        raise ValidationError(f"Field '{field}' has an empty operator expression")
    for operator, operand in condition.items():
        if writing and operator not in WRITE_OPERATORS:
            raise ValidationError(f"Operator '{operator}' is not allowed when updating or deleting")
        if operator in COMPARISON_OPERATORS:
            _check_value(field, operand)
        elif operator in LIST_OPERATORS:
            if not isinstance(operand, list) or not operand or len(operand) > MAX_LIST_LENGTH:
                raise ValidationError(f"Operator '{operator}' needs a non-empty list of at most {MAX_LIST_LENGTH} values")
            for item in operand:
                _check_value(field, item)
        else:
            raise ValidationError(f"Operator '{operator}' is not allowed")


def validate_query(query, depth=0, writing=False):
    """Validate a filter. Returns the query unchanged if it is safe.
    writing=True applies the stricter exact-match-only rules used by update() and delete()."""
    if not isinstance(query, dict):
        raise ValidationError("Query must be a dictionary")
    if depth > MAX_QUERY_DEPTH:
        raise ValidationError("Query is nested too deeply")
    for key, condition in query.items():
        if key in LOGICAL_OPERATORS:
            if not isinstance(condition, list) or not condition or len(condition) > MAX_LIST_LENGTH:
                raise ValidationError(f"'{key}' needs a non-empty list of conditions")
            for sub_query in condition:
                validate_query(sub_query, depth + 1, writing)
        elif key in FIELD_TYPES:
            _check_field_condition(key, condition, writing)
        else:
            raise ValidationError(f"Field or operator '{key}' is not allowed in a query")
    return query


def validate_document(document, require_all=True):
    """Validate a document for create() or the $set data for update()."""
    if not isinstance(document, dict) or not document:
        raise ValidationError("Document must be a non-empty dictionary")
    for field, value in document.items():
        if field not in FIELD_TYPES:
            raise ValidationError(f"Field '{field}' is not allowed")
        _check_value(field, value)
    if require_all:
        missing = [f for f in REQUIRED_ON_CREATE if f not in document]
        if missing:
            raise ValidationError(f"Missing required field(s): {', '.join(missing)}")
    return document


# ---------------------------------------------------------------------------
# CRUD class
# ---------------------------------------------------------------------------
class AnimalShelter:
    def __init__(self, username=None, password=None, read_only=False, collection=None):
        """
        username / password : optional, otherwise MONGO_USER / MONGO_PASSWORD from .env
        read_only           : when True, create/update/delete raise PermissionError
        collection          : optional pre-built collection object, used by the unit tests
                              so they can run without a MongoDB server
        """
        self.read_only = read_only
        self.client = None

        if collection is not None:
            self.collection = collection
            return

        load_dotenv()

        # use credentials passed as parameters, otherwise fall back to .env
        user = username or os.getenv("MONGO_USER")
        password = password or os.getenv("MONGO_PASSWORD")
        host = os.getenv("MONGO_HOST", "localhost")
        port = os.getenv("MONGO_PORT", "27017")
        db_name = os.getenv("MONGO_DATABASE")
        collection_name = os.getenv("MONGO_COLLECTION")

        # fail fast on missing or malformed settings instead of building a broken URI
        if not user or not password:
            raise ValueError("MongoDB credentials are missing (set MONGO_USER and MONGO_PASSWORD)")
        if not db_name or not collection_name:
            raise ValueError("MONGO_DATABASE and MONGO_COLLECTION must be set")
        if not str(port).isdigit():
            raise ValueError("MONGO_PORT must be a number")

        # escape credentials so characters like @ : / in a password cannot alter the URI
        uri = (f"mongodb://{quote_plus(user)}:{quote_plus(password)}@{host}:{port}"
               f"/?authSource={quote_plus(db_name)}")

        try:
            # the client connects lazily, so ping to confirm the server and login really work
            self.client = MongoClient(uri, serverSelectionTimeoutMS=5000)
            self.client.admin.command("ping")
        except PyMongoError as e:
            # report host and port only, never the URI, which contains the password
            raise DatabaseError(f"Could not connect to MongoDB at {host}:{port} ({type(e).__name__})") from e

        self.collection = self.client[db_name][collection_name]

    # -- helpers ------------------------------------------------------------
    def _require_write_access(self):
        if self.read_only:
            raise PermissionError("This connection is read-only")

    @staticmethod
    def _require_filter(query, allow_all):
        # an empty filter matches every document, so make that an explicit choice
        if not query and not allow_all:
            raise ValidationError("An empty filter would affect every record; pass allow_all=True to confirm")

    # -- create -------------------------------------------------------------
    def create(self, data):
        """Insert one validated document. Returns True if MongoDB acknowledged the write."""
        self._require_write_access()
        validate_document(data, require_all=True)
        try:
            return self.collection.insert_one(data).acknowledged
        except PyMongoError as e:
            logger.error("Insert failed: %s", type(e).__name__)
            raise DatabaseError("Could not insert the document") from e

    # -- read ---------------------------------------------------------------
    def read(self, query):
        """Return a list of documents matching a validated query. {} returns every record."""
        validate_query(query)
        try:
            return list(self.collection.find(query))
        except PyMongoError as e:
            logger.error("Read failed: %s", type(e).__name__)
            raise DatabaseError("Could not read from the database") from e

    # -- update -------------------------------------------------------------
    def update(self, query, update_data, allow_all=False):
        """Apply a $set update to matching documents. Returns the number modified."""
        self._require_write_access()
        validate_query(query, writing=True)
        self._require_filter(query, allow_all)
        validate_document(update_data, require_all=False)
        blocked = [f for f in IMMUTABLE_FIELDS if f in update_data]
        if blocked:
            raise ValidationError(f"Field(s) cannot be updated: {', '.join(blocked)}")
        try:
            return self.collection.update_many(query, {"$set": update_data}).modified_count
        except PyMongoError as e:
            logger.error("Update failed: %s", type(e).__name__)
            raise DatabaseError("Could not update the database") from e

    # -- delete -------------------------------------------------------------
    def delete(self, query, allow_all=False):
        """Delete matching documents. Returns the number deleted."""
        self._require_write_access()
        validate_query(query, writing=True)
        self._require_filter(query, allow_all)
        try:
            deleted = self.collection.delete_many(query).deleted_count
        except PyMongoError as e:
            logger.error("Delete failed: %s", type(e).__name__)
            raise DatabaseError("Could not delete from the database") from e
        logger.warning("delete() removed %d document(s)", deleted)   # audit trail for destructive operations
        return deleted

    # -- close --------------------------------------------------------------
    def close(self):
        """Close the database connection. Returns True on success."""
        if self.client is None:
            return True
        try:
            self.client.close()
            logger.info("Client closed")
            return True
        except PyMongoError as e:
            logger.error("Error closing client: %s", type(e).__name__)
            return False
