# app/db/repositories/review_repo.py
from datetime import datetime
from bson import ObjectId
from app.db.mongo import get_db

COLLECTION = "reviews"

def save_reviews(business_id: str, reviews: list[str], analysis: dict) -> dict:
    db = get_db()
    doc = {
        "business_id": business_id,
        "reviews":     reviews,
        "analysis":    analysis,
        "created_at":  datetime.utcnow()
    }
    result = db[COLLECTION].insert_one(doc)
    doc["record_id"] = str(result.inserted_id)
    doc.pop("_id", None)
    return doc

def get_reviews_by_business(business_id: str) -> list[dict]:
    db = get_db()
    docs = db[COLLECTION].find({"business_id": business_id})
    result = []
    for doc in docs:
        doc["record_id"] = str(doc.pop("_id"))
        result.append(doc)
    return result

def get_latest_analysis(business_id: str) -> dict | None:
    db = get_db()
    doc = db[COLLECTION].find_one(
        {"business_id": business_id},
        sort=[("created_at", -1)]
    )
    if doc:
        doc["record_id"] = str(doc.pop("_id"))
    return doc

def delete_reviews_by_business(business_id: str) -> int:
    db = get_db()
    result = db[COLLECTION].delete_many({"business_id": business_id})
    return result.deleted_count