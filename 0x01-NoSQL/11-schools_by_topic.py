#!/usr/bin/env python3
"""Module to find schools by a specific topic."""

from pymongo import MongoClient

def schools_by_topic(mongo_collection, topic):
    """Return a list of schools that have a specific topic.
    
    Args:
        mongo_collection: The pymongo collection object.
        topic (str): The topic searched.

    Returns:
        List of schools with the specific topic.
    """
    schools = list(mongo_collection.find({"topics": topic}))
    return schools
