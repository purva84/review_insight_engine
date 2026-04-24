# app/services/test_sentiment.py
from app.services.sentiment_service import analyze_sentiment, analyze_sentiment_batch, aggregate_sentiment

reviews = [
    "Ordered biryani, took 90 minutes to arrive and was cold. Very disappointed.",
    "Food quality is amazing but delivery was late by 45 minutes again!",
    "Best restaurant in town! Quick delivery and hot food. Will order again.",
    "Packaging was damaged, everything spilled. The food itself smelled great though.",
    "Delivery guy was rude and the order was wrong. Never ordering again.",
]

print("=" * 50)
print("   SENTIMENT ANALYSIS TEST")
print("=" * 50)

# Test single review
print("\nSingle Review Test:")
result = analyze_sentiment(reviews[0])
print(f"  Text    : {reviews[0][:50]}...")
print(f"  Label   : {result['label']}")
print(f"  Score   : {result['score']}")
print(f"  Positive: {result['positive']}")
print(f"  Negative: {result['negative']}")
print(f"  Neutral : {result['neutral']}")

# Test batch
print("\nBatch Analysis:")
batch = analyze_sentiment_batch(reviews)
for r in batch:
    print(f"  [{r['review_id']}] {r['label']:<10} (confidence: {r['score']}) — {r['text'][:40]}...")

# Test aggregate
print("\nAggregated Sentiment:")
agg = aggregate_sentiment(batch)
print(f"  Positive: {agg['positive']}%")
print(f"  Negative: {agg['negative']}%")
print(f"  Neutral : {agg['neutral']}%")
print(f"  Overall : {agg['label']}")
print("=" * 50)