
import requests
import os
import json
from dotenv import load_dotenv


load_dotenv()


API_KEY = os.getenv("GROQ_API_KEY")
API_URL = "https://api.groq.com/openai/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}


SYSTEM_PROMPT = """You are an expert customer review analyst for businesses.


Analyze multiple customer reviews and return ONLY a valid JSON object — no markdown, no explanation, no extra text.


JSON format:
{
  "total_reviews": <int>,
  "overall_sentiment": {
    "positive": <int, percentage>,
    "negative": <int, percentage>,
    "neutral": <int, percentage>,
    "label": "Positive" | "Negative" | "Mixed"
  },
  "top_issues": [
    {
      "issue": "<issue name>",
      "percentage": <int>,
      "count": <int>,
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
}"""




def analyze_reviews(reviews: list[str], business_type: str = "restaurant", focus_areas: list[str] = None) -> dict:
    """
    Analyze multiple reviews and return structured insights.
   
    Args:
        reviews: List of review strings
        business_type: Type of business (restaurant, e-commerce, etc.)
        focus_areas: List of areas to focus on (delivery, quality, price, etc.)
   
    Returns:
        Parsed dict with full structured analysis
    """
    if not reviews:
        raise ValueError("No reviews provided")


    focus = ", ".join(focus_areas) if focus_areas else "general customer experience"
    numbered = "\n".join([f"{i+1}. {r.strip()}" for i, r in enumerate(reviews)])


    user_prompt = f"""Business type: {business_type}
Focus areas: {focus}
Total reviews: {len(reviews)}


Reviews:
{numbered}


Analyze all reviews. Calculate percentages based on {len(reviews)} total reviews. Be specific and data-driven."""


    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        "max_tokens": 1500,
        "temperature": 0.2  # lower = more consistent structured output
    }


    response = requests.post(API_URL, headers=HEADERS, json=payload)


    if response.status_code != 200:
        raise Exception(f"API error {response.status_code}: {response.text}")


    raw = response.json()["choices"][0]["message"]["content"]


    # Strip markdown fences if model adds them
    clean = raw.strip().replace("```json", "").replace("```", "").strip()


    try:
        result = json.loads(clean)


        # DEBUG — remove after fix confirmed
        print(f"DEBUG sentiment raw: pos={result['overall_sentiment']['positive']} neg={result['overall_sentiment']['negative']} neu={result['overall_sentiment']['neutral']}")


        s = result["overall_sentiment"]
        total = s["positive"] + s["negative"] + s["neutral"]
        print(f"DEBUG total={total}, needs fix={total != 100}")


        if total != 100:
            result["overall_sentiment"]["positive"] = round((s["positive"] / total) * 100)
            result["overall_sentiment"]["negative"] = round((s["negative"] / total) * 100)
            result["overall_sentiment"]["neutral"]  = round((s["neutral"]  / total) * 100)
            print(f"DEBUG fixed: pos={result['overall_sentiment']['positive']}% neg={result['overall_sentiment']['negative']}% neu={result['overall_sentiment']['neutral']}%")


        # Normalize issue percentages if LLM returned counts
        n = len(reviews)
        for issue in result.get("top_issues", []):
            if issue["percentage"] <= n:
                issue["percentage"] = round((issue["count"] / n) * 100)


        return result


    except json.JSONDecodeError as e:
        raise Exception(f"Failed to parse JSON response: {e}\nRaw response:\n{raw}")




# Keep old single-review function for backward compatibility
def get_response(prompt: str) -> str:
    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 500,
        "temperature": 0.3
    }
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    if response.status_code != 200:
        raise Exception(f"API error {response.status_code}: {response.text}")
    return response.json()["choices"][0]["message"]["content"]

