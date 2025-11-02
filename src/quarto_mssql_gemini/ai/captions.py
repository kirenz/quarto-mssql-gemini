"""Generate short chart captions using Gemini."""

from __future__ import annotations

from google import genai

from ..config import ConfigurationError, get_gemini_api_key

_caption_client: genai.Client | None = None


def _get_client() -> genai.Client:
    global _caption_client
    if _caption_client is None:
        api_key = get_gemini_api_key()
        try:
            _caption_client = genai.Client(api_key=api_key)
        except Exception as exc:  # pragma: no cover - surface user-friendly error in notebooks
            raise ConfigurationError(f"Failed to initialise Gemini client: {exc}") from exc
    return _caption_client


def generate_chart_caption(data_context: str, metrics: str) -> str:
    """Return a short business-focused caption that highlights chart takeaways."""

    prompt = (
        "You are a business analyst describing a chart for executives.\n\n"
        f"Data Context: {data_context}\n"
        f"Metrics: {metrics}\n\n"
        "Write 2-3 sentences that emphasise the most important movement or comparison "
        "and give a practical implication."
    )

    try:
        response = _get_client().models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
        )
        generated_text = response.text or ""
        return generated_text.strip()
    except Exception as exc:
        return f"Error generating description: {exc}"
