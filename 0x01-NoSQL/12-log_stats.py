#!/usr/bin/env python3
"""Module to provide stats about Nginx logs stored in MongoDB."""

from pymongo import MongoClient

def log_stats():
    """Function to print stats about Nginx logs from a MongoDB collection."""
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.logs
    collection = db.nginx
    
    # Total number of logs
    logs_count = collection.count_documents({})
    print(f"{logs_count} logs")
    
    print("Methods:")
    # Count of documents for each method
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        count = collection.count_documents({"method": method})
        print(f"\tmethod {method}: {count}")
    
    # Count of documents with method=GET and path=/status
    status_check_count = collection.count_documents({"method": "GET", "path": "/status"})
    print(f"{status_check_count} status check")

if __name__ == "__main__":
    log_stats()
