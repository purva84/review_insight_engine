# tests/test_pipeline.py
from app.db.repositories.business_repo import create_business, delete_business
from app.services.pipeline import run_pipeline

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

# Create test business
business = create_business(
    name="Spice Garden",
    business_type="restaurant",
    focus_areas=["delivery", "food quality", "packaging", "price"]
)
print(f"Test business created: {business['business_id']}")

try:
    result = run_pipeline(
        business_id=business["business_id"],
        reviews=reviews
    )

    print("\nFINAL RESULT SUMMARY")
    print("=" * 55)
    print(f"Business       : {result['business']['name']}")
    print(f"Total Reviews  : {result['total_reviews']}")
    print(f"Sentiment      : {result['sentiment']['overall']['label']}")
    print(f"  Positive     : {result['sentiment']['overall']['positive']}%")
    print(f"  Negative     : {result['sentiment']['overall']['negative']}%")
    print(f"  Neutral      : {result['sentiment']['overall']['neutral']}%")
    print(f"Topics Found   : {result['topics']['total']}")
    for t in result["topics"]["list"]:
        print(f"  - {t['label']} ({t['percentage']}%)")
    print(f"Top Issue      : {result['llm_analysis']['top_issues'][0]['issue']} "
          f"({result['llm_analysis']['top_issues'][0]['percentage']}%)")
    print(f"Priority Action: {result['priority_action']}")
    print(f"Record ID      : {result['record_id']}")
    print("=" * 55)

finally:
    # Cleanup
    delete_business(business["business_id"])
    print(f"\nTest business deleted")