#!/usr/bin/env python3
"""This script gathers and displays statistics from Nginx logs stored in a MongoDB database."""

from pymongo import MongoClient

def log_stats():
    """
    Fetches and prints statistics about nginx logs from the MongoDB 'logs' database.
    Statistics include total log entries and counts of different HTTP methods, including a specific check for GET requests to '/status'.
    """
    client = MongoClient('mongodb://127.0.0.1:27017')
    logs_collection = client.logs.nginx
    total = logs_collection.count_documents({})
    get = logs_collection.count_documents({"method": "GET"})
    post = logs_collection.count_documents({"method": "POST"})
    put = logs_collection.count_documents({"method": "PUT"})
    patch = logs_collection.count_documents({"method": "PATCH"})
    delete = logs_collection.count_documents({"method": "DELETE"})
    path = logs_collection.count_documents(
            {"method": "GET", "path": "/status"})
    
    print(f"{total} logs")
    print("Methods:")
    print(f"\tmethod GET: {get}")
    print(f"\tmethod POST: {post}")
    print(f"\tmethod PUT: {put}")
    print(f"\tmethod PATCH: {patch}")
    print(f"\tmethod DELETE: {delete}")
    print(f"{path} status check")

if __name__ == "__main__":
    log_stats()
