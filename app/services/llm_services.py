# app/services/llm_services.py
import requests
import json
from app.core.config import config  # ← single import, all keys available

HEADERS = {
    "Authorization": f"Bearer {config.GROQ_API_KEY}",
    "Content-Type": "application/json"
}

SYSTEM_PROMPT = """You are an expert customer review analyst for businesses.

Analyze multiple customer reviews and return ONLY a valid JSON object — no markdown, no explanation, no extra text.

JSON format:
{
  "total_reviews": <int>,
  "overall_sentiment": {
    "positive": <int, percentage 0-100>,
    "negative": <int, percentage 0-100>,
    "neutral": <int, percentage 0-100>,
    "label": "Positive" | "Negative" | "Mixed"
  },
  "top_issues": [
    {
      "issue": "<issue name>",
      "percentage": <int, % of reviews mentioning this>,
      "count": <int, number of reviews>,
      "severity": "High" | "Medium" | "Low",
      "sample_quote": "<short quote from a review>"
    }
  ],
  "per_review": [
    {
      "review_id": <int>,
      "text": "<original review>",
      "sentiment": "Positive" | "Negative" | "Neutral",
      "score": <float 1.0-5.0>,
      "issues": ["<issue1>", "<issue2>"]
    }
  ],
  "root_cause": "<2-3 sentence root cause analysis>",
  "business_impact": "<1-2 sentence business impact>",
  "recommendations": [
    "<actionable recommendation 1>",
    "<actionable recommendation 2>",
    "<actionable recommendation 3>"
  ],
  "priority_action": "<single most important fix>"
}

IMPORTANT:
- overall_sentiment values must be PERCENTAGES that add up to 100
- percentage in top_issues = (count / total_reviews) * 100"""


def analyze_reviews(reviews: list[str], business_type: str = "restaurant", focus_areas: list[str] = None) -> dict:
    if not reviews:
        raise ValueError("No reviews provided")

    focus = ", ".join(focus_areas) if focus_areas else "general customer experience"
    numbered = "\n".join([f"{i+1}. {r.strip()}" for i, r in enumerate(reviews)])

    user_prompt = f"""Business type: {business_type}
Focus areas: {focus}
Total reviews: {len(reviews)}

Reviews:
{numbered}

Analyze all {len(reviews)} reviews.
- overall_sentiment percentages MUST add up to 100
- top_issues percentage = (count / {len(reviews)}) * 100
- Be specific and data-driven."""

    payload = {
        "model": config.GROQ_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": user_prompt}
        ],
        "max_tokens": config.GROQ_MAX_TOKENS,
        "temperature": config.GROQ_TEMPERATURE
    }

    response = requests.post(config.GROQ_API_URL, headers=HEADERS, json=payload)

    if response.status_code != 200:
        raise Exception(f"API error {response.status_code}: {response.text}")

    raw = response.json()["choices"][0]["message"]["content"]
    clean = raw.strip().replace("```json", "").replace("```", "").strip()

    try:
        result = json.loads(clean)

        # Normalize sentiment percentages
        s = result["overall_sentiment"]
        total = s["positive"] + s["negative"] + s["neutral"]
        if total != 100:
            result["overall_sentiment"]["positive"] = round((s["positive"] / total) * 100)
            result["overall_sentiment"]["negative"] = round((s["negative"] / total) * 100)
            result["overall_sentiment"]["neutral"]  = round((s["neutral"]  / total) * 100)

        # Normalize issue percentages
        n = len(reviews)
        for issue in result.get("top_issues", []):
            if issue["percentage"] <= n:
                issue["percentage"] = round((issue["count"] / n) * 100)

        return result

    except json.JSONDecodeError as e:
        raise Exception(f"Failed to parse JSON: {e}\nRaw: {raw}")


def get_response(prompt: str) -> str:
    payload = {
        "model": config.GROQ_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 500,
        "temperature": 0.3
    }
    response = requests.post(config.GROQ_API_URL, headers=HEADERS, json=payload)
    if response.status_code != 200:
        raise Exception(f"API error {response.status_code}: {response.text}")
    return response.json()["choices"][0]["message"]["content"]