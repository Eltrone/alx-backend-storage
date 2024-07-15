#!/usr/bin/env python3
"""Module to insert a document into a MongoDB collection."""

from pymongo import MongoClient

def insert_school(mongo_collection, **kwargs):
    """Insert a new document into a collection based on kwargs.
    
    Args:
        mongo_collection: The pymongo collection object.
        **kwargs: Arbitrary keyword arguments representing document fields.

    Returns:
        The new _id of the inserted document.
    """
    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id
