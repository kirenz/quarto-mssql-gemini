# PowerPoint Deck

Generate a presentation-ready PPTX with Gemini commentary and exported Altair charts.

## What you'll learn
- Persist charts to `outputs/plots` for slide embedding.
- Call `generate_sales_narrative` to add speaking notes alongside visuals.
- Render with a custom reference deck (`assets/ppt-template.pptx`).

## Run it
1. Double-check your `.env` configuration.
2. From the repository root:  
   `uv run quarto render examples/ppt-deck/ppt-deck.qmd --to pptx`
3. Open the refreshed deck in `examples/ppt-deck/outputs/`.

## Key files
- `ppt-deck.qmd` – Quarto definition of the slide deck.
- `outputs/` – generated PPTX files and supporting PNG charts.
