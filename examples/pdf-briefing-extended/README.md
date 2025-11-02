# Extended PDF Briefing

Produce a longer PDF report with additional charts rendered via Matplotlib.

## What you'll learn
- Aggregate sales metrics for multiple views (monthly, region, category).
- Blend tabular outputs with AI commentary blocks.
- Tune Typst exports for printable deliverables.

## Run it
1. Ensure environment variables are loaded.
2. Execute the render from the repo root:  
   `uv run quarto render examples/pdf-briefing-extended/pdf-briefing-extended.qmd`
3. Inspect `examples/pdf-briefing-extended/outputs/` for the updated PDF.

## Key files
- `pdf-briefing-extended.qmd` – extended Quarto definition.
- `outputs/` – regenerated deliverables.
