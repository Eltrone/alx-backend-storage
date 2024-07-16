#!/usr/bin/env python3
"""
This script provides statistics about Nginx logs stored in a MongoDB database.
It connects to the MongoDB, queries the logs collection, and displays various statistics.
"""

import pymongo

def connect_to_mongodb():
    """
    Establishes a connection to the MongoDB database.
    Returns:
        Collection object for the nginx logs.
    """
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client.logs
    return db.nginx

def display_stats(collection):
    """
    Displays statistics about Nginx logs stored in the MongoDB collection.
    Args:
        collection: The MongoDB collection containing nginx logs.
    """
    # Calculating total number of documents
    total_logs = collection.count_documents({})
    print(f"{total_logs} logs")

    # Displaying methods count
    methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    print("Methods:")
    for method in methods:
        count = collection.count_documents({'method': method})
        print(f"    method {method}: {count}")

    # Counting documents where method=GET and path=/status
    status_checks = collection.count_documents({'method': 'GET', 'path': '/status'})
    print(f"{status_checks} status check")

def main():
    """
    Main function to execute script logic.
    """
    collection = connect_to_mongodb()
    display_stats(collection)

if __name__ == "__main__":
    main()
