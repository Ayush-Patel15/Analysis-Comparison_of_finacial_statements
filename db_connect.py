## All CRUD operation functions related to the mongodb database.

# IMPORTS
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime
import os

# Load the env file
load_dotenv()

# Function to create a connection, with mongodb database
def connect_to_the_database(database):
    try:
        print("Trying to connect to the MongoDb database")
        client = MongoClient(
            os.getenv("MONGODB_URI")
        )
        db = client[database]
        print("Connection successful")
        return db
    except Exception as e:
        print("MongoDb Database connection request falied..!")
        return f"error: {e}"

# Function to create a collection in the databse cluster -> db: database connection variable, collection: name of collection
def create_collection_in_database(db, collection):
    try:
        db.create_collection(collection)
        return f"success: {collection} collection created"
    except Exception as e:
        print("MongoDb create collection request falied..!")
        return f"error: {e}"

# Function to delete a collection from the database cluster
def delete_collection_from_database(db, collection):
    try:
        db[collection].drop()
        return f"success: {collection} collection dropped"
    except Exception as e:
        print("MongoDb drop collection request falied..!")
        return f"error: {e}"

# Function to insert a new data document or update an existing data document in a collection
def insert_and_update_collection(db, collection, identifier, data):
    try:
        cursor = db[collection]
        document = cursor.find_one({identifier: data[identifier]})
        if document:
            data["created_at"] = document["created_at"]
            data["updated_at"] = datetime.now()
            cursor.replace_one({identifier: data[identifier]}, data)
            return "success: data is updated"
        else:
            data["created_at"] = datetime.now()
            data["updated_at"] = datetime.now()
            cursor.insert_one(data)
            return "success: data is inserted"
    except Exception as e:
        print("MongoDb insert or update data in collection request falied..!")
        return f"error: {e}"

# Function to delete all the documents present in a collection
def delete_all_documents_from_collection(db, collection):
    try:
        cursor = db[collection]
        cursor.delete_many({})
        return "success: all documents from the collection deleted"
    except Exception as e:
        print("MongoDb delete documents from collection request falied..!")
        return f"error: {e}"

# if __name__ == "__main__":
#     print(connect_to_the_database("Fundamentals"))
