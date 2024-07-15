#!/usr/bin/env python3
"""Module to update topics of a school document."""

from pymongo import MongoClient

def update_topics(mongo_collection, name, topics):
    """Update the topics of a school document based on the school's name.
    
    Args:
        mongo_collection: The pymongo collection object.
        name (str): The name of the school to update.
        topics (list of str): The new list of topics.

    Returns:
        None
    """
    mongo_collection.update_many({"name": name}, {"$set": {"topics": topics}})
