# app/services/pipeline.py
from app.services.llm_services import analyze_reviews
from app.services.sentiment_service import analyze_sentiment_batch, aggregate_sentiment
from app.services.topic_service import extract_topics, format_topics_for_llm
from app.db.repositories.review_repo import save_reviews
from app.db.repositories.business_repo import get_business

def run_pipeline(business_id: str, reviews: list[str]) -> dict:
    """
    Full pipeline — runs all services and saves to MongoDB.

    Flow:
        reviews
            ↓
        Sentiment Analysis (HuggingFace)
            ↓
        Topic Modeling (BERTopic)
            ↓
        LLM Insight Generation (Groq)
            ↓
        Save to MongoDB
            ↓
        Return full result
    """

    print(f"\n{'='*55}")
    print(f"  PIPELINE STARTED — {len(reviews)} reviews")
    print(f"{'='*55}")

    # Step 1 — fetch business context
    print("\n[1/4] Fetching business context...")
    business = get_business(business_id)
    if not business:
        raise Exception(f"Business not found: {business_id}")
    print(f"  Business : {business['name']}")
    print(f"  Type     : {business['business_type']}")
    print(f"  Focus    : {', '.join(business['focus_areas'])}")

    # Step 2 — sentiment analysis
    print("\n[2/4] Running sentiment analysis (HuggingFace)...")
    try:
        sentiment_results = analyze_sentiment_batch(reviews)
        aggregated = aggregate_sentiment(sentiment_results)
        print(f"  Overall  : {aggregated['label']}")
        print(f"  Positive : {aggregated['positive']}%")
        print(f"  Negative : {aggregated['negative']}%")
        print(f"  Neutral  : {aggregated['neutral']}%")
    except Exception as e:
        print(f"  Sentiment failed: {e} — skipping")
        sentiment_results = []
        aggregated = {"positive": 0, "negative": 0, "neutral": 0, "label": "Unknown"}

    # Step 3 — topic modeling
    print("\n[3/4] Running topic modeling (BERTopic)...")
    try:
        topic_result = extract_topics(reviews, min_topic_size=2)
        topics_for_llm = format_topics_for_llm(topic_result)
        print(f"  Topics found : {topic_result['total_topics']}")
        for t in topic_result["topics"]:
            print(f"  - {t['label']} ({t['percentage']}%)")
    except Exception as e:
        print(f"  Topics failed: {e} — skipping")
        topic_result = {"topics": [], "outliers": [], "total_topics": 0}
        topics_for_llm = "No topics found"

    # Step 4 — LLM insight generation
    print("\n[4/4] Generating insights (Groq LLM)...")
    llm_result = analyze_reviews(
        reviews=reviews,
        business_type=business["business_type"],
        focus_areas=business["focus_areas"]
    )
    print(f"  Priority Action: {llm_result['priority_action']}")

    # Step 5 — combine all results
    final_result = {
        "business": {
            "business_id":   business_id,
            "name":          business["name"],
            "business_type": business["business_type"],
            "focus_areas":   business["focus_areas"]
        },
        "total_reviews": len(reviews),
        "sentiment": {
            "overall":    aggregated,
            "per_review": sentiment_results
        },
        "topics": {
            "total":    topic_result["total_topics"],
            "list":     topic_result["topics"],
            "outliers": topic_result["outliers"]
        },
        "llm_analysis": llm_result,
        "priority_action": llm_result["priority_action"]
    }

    # Step 6 — save to MongoDB
    print("\n  Saving to MongoDB...")
    saved = save_reviews(business_id, reviews, final_result)
    final_result["record_id"] = saved["record_id"]
    print(f"  Saved — record ID: {saved['record_id']}")

    print(f"\n{'='*55}")
    print(f"  PIPELINE COMPLETE")
    print(f"{'='*55}\n")

    return final_result