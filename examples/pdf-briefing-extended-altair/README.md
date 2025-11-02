# Extended PDF (Altair)

Render the extended PDF briefing while exporting charts with Altair for crisp vector imagery.

## What you'll learn
- Save reusable Altair charts into `outputs/plots` for embedding.
- Reuse the same data prep as the Matplotlib version with interactive visuals.
- Generate AI narratives for each section via `generate_sales_narrative`.

## Run it
1. Confirm credentials in `.env`.
2. From the project root:  

```bash
uv run quarto render examples/pdf-briefing-extended-altair/pdf-briefing-extended-altair.qmd
```

3. Check the refreshed PDF and PNG assets under `examples/pdf-briefing-extended-altair/outputs/`.

## Key files

- `pdf-briefing-extended-altair.qmd` – Altair-first Quarto file.
- `outputs/plots/` – exported chart images consumed by the PDF.
