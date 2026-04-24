# tests/test_db.py
from app.db.mongo import ping
from app.db.repositories.business_repo import (
    create_business, get_business, get_all_businesses, delete_business
)
from app.db.repositories.review_repo import (
    save_reviews, get_reviews_by_business, get_latest_analysis
)

print("=" * 55)
print("   MONGODB TEST")
print("=" * 55)

# Step 1 — ping
print("\nStep 1 — Ping MongoDB:")
ping()

# Step 2 — create business
print("\nStep 2 — Create Business:")
business = create_business(
    name="Spice Garden",
    business_type="restaurant",
    focus_areas=["delivery", "food quality", "packaging"]
)
print(f"  Created: {business['name']} — ID: {business['business_id']}")

# Step 3 — fetch business
print("\nStep 3 — Fetch Business:")
fetched = get_business(business["business_id"])
print(f"  Fetched: {fetched['name']} | Type: {fetched['business_type']}")

# Step 4 — save reviews + analysis
print("\nStep 4 — Save Reviews + Analysis:")
reviews = [
    "Delivery was late by 90 minutes. Food was cold.",
    "Amazing food quality! Will order again.",
    "Packaging was damaged, everything spilled."
]
mock_analysis = {
    "total_reviews": 3,
    "overall_sentiment": {"positive": 33, "negative": 67, "neutral": 0, "label": "Negative"},
    "top_issues": [{"issue": "Delivery", "percentage": 67, "count": 2, "severity": "High"}],
    "priority_action": "Fix delivery times"
}
saved = save_reviews(business["business_id"], reviews, mock_analysis)
print(f"  Saved record ID: {saved['record_id']}")

# Step 5 — fetch latest analysis
print("\nStep 5 — Fetch Latest Analysis:")
latest = get_latest_analysis(business["business_id"])
print(f"  Priority Action: {latest['analysis']['priority_action']}")
print(f"  Total Reviews  : {latest['analysis']['total_reviews']}")

# Step 6 — get all businesses
print("\nStep 6 — All Businesses:")
all_biz = get_all_businesses()
print(f"  Total businesses in DB: {len(all_biz)}")

# Step 7 — cleanup test data
print("\nStep 7 — Cleanup:")
delete_business(business["business_id"])
print(f"  Deleted business: {business['name']}")

print("\n  All MongoDB tests passed!")
print("=" * 55)