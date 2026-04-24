# tests/test_topics.py
from app.services.topic_service import extract_topics, format_topics_for_llm

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

print("=" * 55)
print("   TOPIC MODELING TEST")
print("=" * 55)

result = extract_topics(reviews, min_topic_size=2)

print(f"\nTotal Topics Found: {result['total_topics']}")

print("\nTopics:")
for t in result["topics"]:
    bar = "#" * (t["percentage"] // 5)
    print(f"\n  Topic {t['topic_id']}: {t['label']}")
    print(f"  Keywords   : {', '.join(t['keywords'])}")
    print(f"  Frequency  : {t['percentage']}% ({t['count']} reviews) {bar}")
    print(f"  Reviews    :")
    for r in t["reviews"]:
        print(f"    - {r[:60]}...")

if result["outliers"]:
    print(f"\nOutliers ({len(result['outliers'])} reviews didn't fit any topic):")
    for r in result["outliers"]:
        print(f"  - {r[:60]}...")

print("\nFormatted for LLM:")
print(format_topics_for_llm(result))

print("=" * 55)