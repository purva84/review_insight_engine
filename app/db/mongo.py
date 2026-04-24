# app/db/mongo.py
from pymongo import MongoClient
from pymongo.database import Database
from app.core.config import config

_client: MongoClient = None

def get_client() -> MongoClient:
    global _client
    if _client is None:
        _client = MongoClient(config.MONGO_URI)
    return _client

def get_db() -> Database:
    client = get_client()
    return client[config.MONGO_DB]

def ping():
    try:
        get_client().admin.command("ping")
        print(f"MongoDB connected — {config.MONGO_URI}")
        return True
    except Exception as e:
        print(f"MongoDB connection failed: {e}")
        return False