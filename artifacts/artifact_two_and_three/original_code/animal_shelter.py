"""
Animal Shelter CRUD Module
Provides Create, Read, Update, and Delete operations for MongoDB shelter database.
Supports authentication via environment variables or direct credential passing.
"""

from pymongo import MongoClient
from dotenv import load_dotenv
import os

class AnimalShelter:
    def __init__(self, username=None, password=None):
        # load environment variables
        load_dotenv()

        # Use username and password if passed as parameters
        if username and password:
            self.USER = username
            self.PASSWORD = password
        # If not passed as parameters use username and password from .env
        else:
            self.USER = os.getenv("MONGO_USER")
            self.PASSWORD = os.getenv("MONGO_PASSWORD")

        # create connection variables

        HOST = os.getenv("MONGO_HOST", "localhost")
        PORT = os.getenv("MONGO_PORT", "27017")
        DB = os.getenv("MONGO_DATABASE")
        COLLECTION = os.getenv("MONGO_COLLECTION")

        # create connection string
        uri = f"mongodb://{self.USER}:{self.PASSWORD}@{HOST}:{PORT}"


        try:
            # initialize connection
            self.client = MongoClient(uri)
            self.database = self.client[DB]
            self.collection = self.database[COLLECTION]
        # exception handling for failed connection
        except Exception as e:
            raise Exception(f"Connection to MongoDB failed: {e}")

    # create method for data insertion
    def create(self, data):
        try:
            if data is not None:
                result = self.collection.insert_one(data)
                return result.acknowledged
            else:
                raise ValueError("Data parameter is required")
        except Exception as e:
            print(f"Error inserting document: {e}")
            return False

    # read method - returns list of documents
    def read(self, query):
        try:
            if query is not None:
                # find() returns a cursor, convert to list
                cursor = self.collection.find(query)
                results = list(cursor)
                return results
            else:
                raise ValueError("Query parameter is required")
        except Exception as e:
            print(f"Error reading documents: {e}")
            # Return empty list on error
            return []

    # update method - updates document(s)
    def update(self, query, update_data):
        try:
            if query is not None and update_data is not None:
                # Use $set operator to update fields
                result = self.collection.update_many(query, {"$set": update_data})
                return result.modified_count  # return number of documents modified
            else:
                raise ValueError("Both query and update_data parameters are required")
        except Exception as e:
            print(f"Error updating documents: {e}")
            return 0

    # delete method - deletes document(s)
    def delete(self, query):
        try:
            if query is not None:
                result = self.collection.delete_many(query)
                return result.deleted_count # return number of documents deleted
            else:
                raise ValueError("Query parameter is required")
        except Exception as e:
            print(f"Error deleting documents: {e}")
            return 0

    # close method - manually closes db connection
    # Optional: Refactor for automatic connection cleanup
    def close(self):
        try:
            self.client.close()
            print("Client closed")
            return True
        except Exception as e:
            print(f"Error closing client: {e}")