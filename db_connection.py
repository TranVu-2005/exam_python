from pymongo import MongoClient

# Connect to MongoDB
def connect_to_db():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["medical_service"]
    return db
