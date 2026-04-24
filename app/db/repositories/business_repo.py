# app/db/repositories/business_repo.py
from datetime import datetime
from bson import ObjectId
from app.db.mongo import get_db

COLLECTION = "businesses"

def create_business(name: str, business_type: str, focus_areas: list[str]) -> dict:
    db = get_db()
    doc = {
        "name":          name,
        "business_type": business_type,
        "focus_areas":   focus_areas,
        "created_at":    datetime.utcnow()
    }
    result = db[COLLECTION].insert_one(doc)
    doc["business_id"] = str(result.inserted_id)
    doc.pop("_id", None)
    return doc

def get_business(business_id: str) -> dict | None:
    db = get_db()
    doc = db[COLLECTION].find_one({"_id": ObjectId(business_id)})
    if doc:
        doc["business_id"] = str(doc.pop("_id"))
    return doc

def get_all_businesses() -> list[dict]:
    db = get_db()
    docs = db[COLLECTION].find()
    result = []
    for doc in docs:
        doc["business_id"] = str(doc.pop("_id"))
        result.append(doc)
    return result

def delete_business(business_id: str) -> bool:
    db = get_db()
    result = db[COLLECTION].delete_one({"_id": ObjectId(business_id)})
    return result.deleted_count > 0