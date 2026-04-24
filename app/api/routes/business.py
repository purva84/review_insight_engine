# app/api/routes/business.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.db.repositories.business_repo import (
    create_business, get_business, get_all_businesses, delete_business
)

router = APIRouter(prefix="/business", tags=["Business"])

class BusinessInput(BaseModel):
    name: str
    business_type: str
    focus_areas: list[str]

@router.post("/register")
def register_business(data: BusinessInput):
    try:
        business = create_business(data.name, data.business_type, data.focus_areas)
        return {"success": True, "business": business}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/all")
def list_businesses():
    try:
        businesses = get_all_businesses()
        return {"success": True, "businesses": businesses}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{business_id}")
def fetch_business(business_id: str):
    business = get_business(business_id)
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")
    return {"success": True, "business": business}

@router.delete("/{business_id}")
def remove_business(business_id: str):
    deleted = delete_business(business_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Business not found")
    return {"success": True, "message": "Business deleted"}