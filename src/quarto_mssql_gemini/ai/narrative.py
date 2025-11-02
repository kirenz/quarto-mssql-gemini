"""Generate business-ready narratives using Gemini."""

from __future__ import annotations

from google import genai

from ..config import ConfigurationError, get_gemini_api_key

_client_instance: genai.Client | None = None


def _get_client() -> genai.Client:
    global _client_instance
    if _client_instance is None:
        api_key = get_gemini_api_key()
        try:
            _client_instance = genai.Client(api_key=api_key)
        except Exception as exc:  # pragma: no cover - surface user-friendly error in notebooks
            raise ConfigurationError(f"Failed to initialise Gemini client: {exc}") from exc
    return _client_instance


def generate_sales_narrative(data_context: str, metrics: str) -> str:
    """Return a concise narrative describing the provided sales metrics."""

    prompt = (
        "You are an experienced business analyst providing clear, data-driven insights "
        "with specific numbers and actionable recommendations.\n\n"
        f"Context: {data_context}\n\n"
        "Key Performance Metrics:\n"
        f"{metrics}\n\n"
        "Provide a 2-4 sentence analysis that:\n"
        "1. Highlights the most significant insight(s)\n"
        "2. Connects the metrics to a potential business implication or recommendation"
    )

    try:
        response = _get_client().models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
        )
        generated_text = response.text or ""
        return generated_text.strip()
    except Exception as exc:
        return f"Error generating analysis: {exc}"
