"""
Centralized application configuration.

Loads environment variables (optionally via python-dotenv) and exposes
a typed AppConfig object that can be imported anywhere in the codebase.
"""


from dataclasses import dataclass
import os

try:
    # Optional dependency: python-dotenv
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    # If python-dotenv is not installed, environment variables must be set manually.
    pass


@dataclass(frozen=True)
class AppConfig:
    """Application-wide configuration."""

    app_name: str
    model_name: str
    google_api_key: str

    @property
    def has_valid_api_key(self) -> bool:
        return bool(self.google_api_key)


def _load_config() -> AppConfig:
    app_name = os.getenv("APP_NAME", "agentic_ai_tutor_with_googleadk")
    model_name = os.getenv("GEMINI_MODEL_NAME", "gemini-2.5-flash-lite")
    google_api_key = os.getenv("GOOGLE_API_KEY", "")

    if not google_api_key:
        raise RuntimeError(
            "GOOGLE_API_KEY is not set. Define it in your environment or .env file."
        )

    return AppConfig(
        app_name=app_name,
        model_name=model_name,
        google_api_key=google_api_key,
    )


config: AppConfig = _load_config()
