#!/usr/bin/env python3
"""
Interaction with MongoDB using pymongo
Statistics extraction for Nginx logs within a MongoDB collection
"""

from pymongo import MongoClient

if __name__ == "__main__":
    # Establish MongoDB connection
    mongo_client = MongoClient('mongodb://127.0.0.1:27017')

    # Get access to the nginx logs collection
    nginx_collection = mongo_client.logs.nginx

    # Retrieve and display the total count of log entries
    log_count = nginx_collection.count_documents({})
    print(f'{log_count} logs')

    # Enumerate and count logs by HTTP method types
    http_methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print('Methods:')
    for method in http_methods:
        method_count = nginx_collection.count_documents({"method": method})
        print(f'\tmethod {method}: {method_count}')

    # Determine the number of GET requests for the '/status' path
    get_status_count = nginx_collection.count_documents({"method": "GET", "path": "/status"})
    print(f'{get_status_count} status check')
