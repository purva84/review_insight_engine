# app/api/routes/reviews.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.pipeline import run_pipeline
from app.db.repositories.review_repo import (
    save_reviews, get_latest_analysis, get_reviews_by_business
)
from app.db.repositories.business_repo import get_business

router = APIRouter(prefix="/reviews", tags=["Reviews"])

class ReviewInput(BaseModel):
    business_id: str
    reviews: list[str]

@router.post("/analyze")
def analyze(data: ReviewInput):
    try:
        if not data.reviews:
            raise HTTPException(status_code=400, detail="No reviews provided")
        if len(data.reviews) < 3:
            raise HTTPException(status_code=400, detail="Minimum 3 reviews required")

        result = run_pipeline(
            business_id=data.business_id,
            reviews=data.reviews
        )
        return {"success": True, "result": result}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/latest/{business_id}")
def latest_analysis(business_id: str):
    result = get_latest_analysis(business_id)
    if not result:
        raise HTTPException(status_code=404, detail="No analysis found")
    return {"success": True, "analysis": result}

@router.get("/history/{business_id}")
def analysis_history(business_id: str):
    results = get_reviews_by_business(business_id)
    return {"success": True, "count": len(results), "history": results}