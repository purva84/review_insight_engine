# app/api/routes/reviews.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.llm_services import analyze_reviews
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
        # Fetch business context
        business = get_business(data.business_id)
        if not business:
            raise HTTPException(status_code=404, detail="Business not found")

        # Run LLM analysis
        result = analyze_reviews(
            reviews=data.reviews,
            business_type=business["business_type"],
            focus_areas=business["focus_areas"]
        )

        # Save to MongoDB
        saved = save_reviews(data.business_id, data.reviews, result)

        return {
            "success":   True,
            "record_id": saved["record_id"],
            "analysis":  result
        }
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