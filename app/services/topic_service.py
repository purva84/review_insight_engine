# app/services/topic_service.py
from bertopic import BERTopic
from sklearn.feature_extraction.text import CountVectorizer

def extract_topics(reviews: list[str], min_topic_size: int = 2) -> dict:
    if len(reviews) < 3:
        raise ValueError("Need at least 3 reviews for topic modeling")

    vectorizer = CountVectorizer(
        stop_words="english",
        min_df=1,
        ngram_range=(1, 1)       # single words only — fixes repetitive labels
    )

    topic_model = BERTopic(
        vectorizer_model=vectorizer,
        min_topic_size=min_topic_size,
        nr_topics="auto",
        verbose=False
    )

    topics, probs = topic_model.fit_transform(reviews)
    topic_info = topic_model.get_topic_info()

    results = []
    outlier_reviews = []

    for _, row in topic_info.iterrows():
        topic_id = row["Topic"]

        if topic_id == -1:
            outlier_reviews = [
                reviews[i] for i, t in enumerate(topics) if t == -1
            ]
            continue

        topic_words = topic_model.get_topic(topic_id)

        # Deduplicate keywords
        seen = set()
        keywords = []
        for word, _ in topic_words:
            if word not in seen:
                seen.add(word)
                keywords.append(word)
            if len(keywords) == 5:
                break

        label = " + ".join(keywords[:3])   # cleaner label e.g. "delivery + late + cold"

        topic_reviews = [
            reviews[i] for i, t in enumerate(topics) if t == topic_id
        ]

        count = len(topic_reviews)
        percentage = round((count / len(reviews)) * 100)

        results.append({
            "topic_id":   topic_id,
            "label":      label,
            "keywords":   keywords,
            "count":      count,
            "percentage": percentage,
            "reviews":    topic_reviews
        })

    results.sort(key=lambda x: x["count"], reverse=True)

    # Re-assign outliers to nearest topic if too many
    if len(outlier_reviews) > len(reviews) * 0.4:
        print(f"  Note: {len(outlier_reviews)} outliers — consider adding more reviews for better topics")

    return {
        "topics":       results,
        "outliers":     outlier_reviews,
        "total_topics": len(results)
    }


def format_topics_for_llm(topic_result: dict) -> str:
    lines = []
    for t in topic_result["topics"]:
        lines.append(
            f"Topic: {t['label']} | {t['percentage']}% of reviews "
            f"({t['count']} reviews) | Keywords: {', '.join(t['keywords'])}"
        )
    return "\n".join(lines)