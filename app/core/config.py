# app/core/config.py
import os
from pathlib import Path
from dotenv import load_dotenv

# Always load from project root regardless of where script is run from
load_dotenv(dotenv_path=Path(__file__).resolve().parents[2] / ".env")

class Config:
    # --- Groq LLM ---
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_API_URL: str = "https://api.groq.com/openai/v1/chat/completions"
    GROQ_MODEL: str   = "llama-3.1-8b-instant"
    GROQ_MAX_TOKENS: int = 1500
    GROQ_TEMPERATURE: float = 0.2

    # --- HuggingFace (for sentiment + embeddings ) ---
    HF_API_KEY: str   = os.getenv("HUGGINGFACEHUB_API_TOKEN", "")
    HF_API_URL: str   = "https://api-inference.huggingface.co/models"

    # --- MongoDB ---
    MONGO_URI: str    = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    MONGO_DB: str     = os.getenv("MONGO_DB", "review_insight_engine")

    # --- App ---
    APP_NAME: str     = "Review Insight Engine"
    DEBUG: bool       = os.getenv("DEBUG", "false").lower() == "true"

config = Config()