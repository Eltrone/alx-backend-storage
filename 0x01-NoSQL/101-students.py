#!/usr/bin/env python3
"""Module for function top_students which fetches student records sorted by average score."""

from pymongo import MongoClient

def top_students(mongo_collection):
    """
    Returns all students sorted by average score.
    
    Args:
        mongo_collection: A pymongo collection object representing the students.
        
    Returns:
        List of students sorted by their average score with each student record including the 'averageScore'.
    """
    pipeline = [
        {
            "$unwind": "$topics"
        },
        {
            "$group": {
                "_id": "$_id",
                "name": { "$first": "$name" },
                "averageScore": { "$avg": "$topics.score" }
            }
        },
        {
            "$sort": { "averageScore": -1 }
        }
    ]
    results = mongo_collection.aggregate(pipeline)
    return list(results)

if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    students_collection = client.my_db.students
    top_students_list = top_students(students_collection)
    for student in top_students_list:
        print("[{}] {} => {}".format(student.get('_id'), student.get('name'), student.get('averageScore')))
