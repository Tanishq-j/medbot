"""Configuration management for MedBot.

Supports both Google Gemini (recommended for fast multimodal clinical analysis) and Groq.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env file if present
load_dotenv(BASE_DIR / ".env", override=True)

# Provider selection: "google" or "groq"
GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "").strip()
GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "").strip()

# Default to google if GEMINI_API_KEY is provided, else fallback to groq
default_provider = "google" if GEMINI_API_KEY else "groq"
MODEL_PROVIDER: str = os.getenv("MODEL_PROVIDER", default_provider).strip().lower()

GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-3.8-flash").strip()
GROQ_MODEL: str = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b").strip()

HOST: str = os.getenv("HOST", "127.0.0.1").strip()
PORT: int = int(os.getenv("PORT", "8000").strip())
REQUEST_TIMEOUT: int = int(os.getenv("REQUEST_TIMEOUT", "90").strip())

MEDICAL_DISCLAIMER: str = (
    "Disclaimer: MedBot provides educational and informational medical guidance based on established clinical guidelines. "
    "It does not constitute formal medical diagnosis, treatment, prescription, or a doctor-patient relationship. "
    "Always consult a licensed healthcare professional for medical concerns or emergency services for acute medical situations."
)

# Alias for backwards compatibility
LEGAL_DISCLAIMER: str = MEDICAL_DISCLAIMER


def is_provider_configured() -> bool:
    """Check if the active model provider has a valid API key configured."""
    dummy_values = {"", "your_groq_api_key_here", "your_gemini_api_key_here", "placeholder"}
    if MODEL_PROVIDER == "google":
        return bool(GEMINI_API_KEY and GEMINI_API_KEY not in dummy_values)
    return bool(GROQ_API_KEY and GROQ_API_KEY not in dummy_values)


def is_groq_configured() -> bool:
    """Backward compatibility helper for health checks."""
    return is_provider_configured()


def get_active_model_name() -> str:
    """Return the name of the currently active model."""
    if MODEL_PROVIDER == "google":
        return f"Google ({GEMINI_MODEL})"
    return f"Groq ({GROQ_MODEL})"
