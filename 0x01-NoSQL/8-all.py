#!/usr/bin/env python3
"""Module to list all documents in a MongoDB collection."""

def list_all(mongo_collection):
    """List all documents in a given collection.
    
    Args:
        mongo_collection (pymongo.collection.Collection): The collection to search.

    Returns:
        list: A list of documents found in the collection, or an empty list if no documents found.
    """
    documents = list(mongo_collection.find())
    return documents if documents else []

if __name__ == "__main__":
    # This part of code will not be executed when imported, it's for testing purpose.
    from pymongo import MongoClient
    client = MongoClient('mongodb://127.0.0.1:27017')
    school_collection = client.my_db.school
    schools = list_all(school_collection)
    for school in schools:
        print("[{}] {}".format(school.get('_id'), school.get('name')))
