# PDF Briefing

Create a short-form PDF briefing that highlights the current period's Germany sales performance.

## What you'll learn
- Query the Germany slice of the dataset and prepare reporting tables.
- Ask Gemini for structured narrative context with `generate_sales_narrative`.
- Export a Typst PDF using Quarto.

## Run it
1. Confirm your environment is configured (database + Gemini credentials).
2. From the repository root:  

```bash
uv run quarto render examples/pdf-briefing/pdf-briefing.qmd
```

3. Review `examples/pdf-briefing/outputs/pdf-briefing.pdf`.

## Key files
- `pdf-briefing.qmd` – Quarto source for the briefing pack.
- `outputs/` – regenerated PDFs and any intermediate artifacts.
