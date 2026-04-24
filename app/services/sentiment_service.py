# app/services/sentiment_service.py
import requests
from app.core.config import config

SENTIMENT_URL = "https://router.huggingface.co/hf-inference/models/cardiffnlp/twitter-roberta-base-sentiment-latest"

HEADERS = {
    "Authorization": f"Bearer {config.HF_API_KEY}",
    "Content-Type": "application/json"
}

# Map HF labels to readable labels
LABEL_MAP = {
    "positive": "Positive",
    "negative": "Negative",
    "neutral":  "Neutral"
}

def analyze_sentiment(text: str) -> dict:
    """
    Analyze sentiment of a single review.
    
    Returns:
        {
            "label": "Positive" | "Negative" | "Neutral",
            "score": 0.98,         # confidence 0-1
            "positive": 0.91,      # individual scores
            "negative": 0.05,
            "neutral":  0.04
        }
    """
    payload = {"inputs": text}
    response = requests.post(SENTIMENT_URL, headers=HEADERS, json=payload)

    if response.status_code != 200:
        raise Exception(f"Sentiment API error {response.status_code}: {response.text}")

    result = response.json()

    # HF returns list of list of dicts
    # [[{"label": "positive", "score": 0.91}, ...]]
    scores = result[0]

    # Build readable dict
    score_dict = {item["label"].lower(): round(item["score"], 4) for item in scores}

    # Get dominant label
    top = max(scores, key=lambda x: x["score"])
    label = LABEL_MAP.get(top["label"].lower(), top["label"])

    return {
        "label":    label,
        "score":    round(top["score"], 4),
        "positive": score_dict.get("positive", 0.0),
        "negative": score_dict.get("negative", 0.0),
        "neutral":  score_dict.get("neutral",  0.0)
    }


def analyze_sentiment_batch(reviews: list[str]) -> list[dict]:
    """
    Analyze sentiment for multiple reviews.
    
    Returns:
        List of sentiment dicts, one per review
    """
    results = []
    for i, review in enumerate(reviews):
        try:
            sentiment = analyze_sentiment(review)
            sentiment["review_id"] = i + 1
            sentiment["text"] = review
            results.append(sentiment)
        except Exception as e:
            # Don't fail entire batch for one bad review
            results.append({
                "review_id": i + 1,
                "text":      review,
                "label":     "Unknown",
                "score":     0.0,
                "positive":  0.0,
                "negative":  0.0,
                "neutral":   0.0,
                "error":     str(e)
            })
    return results


def aggregate_sentiment(sentiment_results: list[dict]) -> dict:
    """
    Aggregate per-review sentiments into overall percentages.
    
    Returns:
        {
            "positive": 30,
            "negative": 50,
            "neutral":  20,
            "label":    "Negative"
        }
    """
    total = len(sentiment_results)
    if total == 0:
        return {"positive": 0, "negative": 0, "neutral": 0, "label": "Unknown"}

    counts = {"positive": 0, "negative": 0, "neutral": 0}
    for r in sentiment_results:
        label = r["label"].lower()
        if label in counts:
            counts[label] += 1

    percentages = {k: round((v / total) * 100) for k, v in counts.items()}

    # Determine overall label
    top_label = max(counts, key=counts.get)
    if counts["positive"] > 0 and counts["negative"] > 0:
        label = "Mixed" if abs(counts["positive"] - counts["negative"]) <= 2 else top_label.capitalize()
    else:
        label = top_label.capitalize()

    return {
        "positive": percentages["positive"],
        "negative": percentages["negative"],
        "neutral":  percentages["neutral"],
        "label":    label
    }