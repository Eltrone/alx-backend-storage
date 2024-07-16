#!/usr/bin/env python3
import pymongo

def main():
    """ Connect to MongoDB and display statistics about nginx logs. """
    # Connexion à MongoDB
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client.logs
    collection = db.nginx

    # Calculer le nombre total de documents
    total_logs = collection.count_documents({})
    print(f"{total_logs} logs")

    # Méthodes HTTP à compter
    methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    print("Methods:")
    for method in methods:
        count = collection.count_documents({'method': method})
        print(f"    method {method}: {count}")

    # Compter les requêtes spécifiques pour GET /status
    status_checks = collection.count_documents({'method': 'GET', 'path': '/status'})
    print(f"{status_checks} status check")

if __name__ == "__main__":
    main()
