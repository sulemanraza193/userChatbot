from pymongo import MongoClient
from .config import MONGODB_URI, DATABASE_NAME


client = MongoClient(MONGODB_URI)

db = client[DATABASE_NAME]

users_collection = db["users"]
admins_collection = db["admins"]


def check_database():
    client.admin.command("ping")
    print("MongoDB connected")