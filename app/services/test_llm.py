# app/services/test_llm.py
import traceback
from app.services.llm_services import analyze_reviews


reviews = [
    "Ordered biryani, took 90 minutes to arrive and was cold. Very disappointed.",
    "Food quality is amazing but delivery was late by 45 minutes again!",
    "Best restaurant in town! Quick delivery and hot food. Will order again.",
    "Packaging was damaged, everything spilled. The food itself smelled great though.",
    "Delivery guy was rude and the order was wrong. Never ordering again.",
    "Fantastic paneer tikka! Arrived in 30 minutes and tasted fresh.",
    "Third time ordering, third time delivery is late. Fix your logistics!",
    "Price is too high for the portion size. Food quality is decent.",
    "Staff was super helpful when I called about my order. Food was good too.",
    "Cold food, wrong items, late delivery. Complete disaster of an experience."
]


print("Starting analysis...")  # checkpoint 1


try:
    result = analyze_reviews(
        reviews=reviews,
        business_type="restaurant",
        focus_areas=["delivery", "food quality", "packaging", "price"]
    )
    print("Got result from API...")  # checkpoint 2
    print("Raw result:", result)     # checkpoint 3 — print raw before formatting


    print("=" * 55)
    print("   REVIEW INSIGHT ENGINE — ANALYSIS RESULTS")
    print("=" * 55)


    print(f"\nTotal Reviews Analyzed : {result['total_reviews']}")


    s = result["overall_sentiment"]
    print(f"\nOverall Sentiment      : {s['label']}")
    print(f"  Positive             : {s['positive']}%")
    print(f"  Negative             : {s['negative']}%")
    print(f"  Neutral              : {s['neutral']}%")


    print(f"\nTop Issues:")
    for issue in result["top_issues"]:
        bar = "#" * (issue["percentage"] // 5)
        print(f"  [{issue['severity']}] {issue['issue']:<25} {issue['percentage']}% {bar}")
        print(f"         \"{issue['sample_quote']}\"")


    print(f"\nPer-Review Breakdown:")
    print(f"  {'#':<4} {'Sentiment':<10} {'Score':<7} Issues")
    print(f"  {'-'*50}")
    for r in result["per_review"]:
        issues = ", ".join(r["issues"]) if r["issues"] else "none"
        print(f"  {r['review_id']:<4} {r['sentiment']:<10} {r['score']:<7} {issues}")


    print(f"\nRoot Cause:")
    print(f"  {result['root_cause']}")


    print(f"\nBusiness Impact:")
    print(f"  {result['business_impact']}")


    print(f"\nRecommendations:")
    for i, rec in enumerate(result["recommendations"], 1):
        print(f"  {i}. {rec}")


    print(f"\nPriority Action:")
    print(f"  >> {result['priority_action']}")
    print("=" * 55)


except Exception as e:
    print(f"\nERROR: {e}")
    traceback.print_exc()





