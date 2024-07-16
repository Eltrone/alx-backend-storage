#!/usr/bin/env python3
"""Provides statistics about Nginx logs stored in MongoDB, including the top 10 most frequent IP addresses."""

from pymongo import MongoClient

def log_stats():
    """Log statistics function including a list of the top 10 most frequent IPs."""
    client = MongoClient('mongodb://127.0.0.1:27017')
    logs_collection = client.logs.nginx
    total = logs_collection.count_documents({})
    get = logs_collection.count_documents({"method": "GET"})
    post = logs_collection.count_documents({"method": "POST"})
    put = logs_collection.count_documents({"method": "PUT"})
    patch = logs_collection.count_documents({"method": "PATCH"})
    delete = logs_collection.count_documents({"method": "DELETE"})
    status_check = logs_collection.count_documents({"method": "GET", "path": "/status"})
    
    # Aggregate top 10 IP addresses
    top_ips = logs_collection.aggregate([
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ])

    print(f"{total} logs")
    print("Methods:")
    print(f"\tmethod GET: {get}")
    print(f"\tmethod POST: {post}")
    print(f"\tmethod PUT: {put}")
    print(f"\tmethod PATCH: {patch}")
    print(f"\tmethod DELETE: {delete}")
    print(f"{status_check} status check")
    print("IPs:")
    for ip in top_ips:
        print(f"\t{ip['_id']}: {ip['count']}")

if __name__ == "__main__":
    log_stats()
