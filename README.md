# Quarto MSSQL Gemini Starter

Ready-to-share Quarto examples that combine Microsoft SQL Server data with Gemini-generated commentary. The repo is structured so newcomers can find the right helper, render a deliverable, and iterate without digging through notebooks.

## Before you start
- Install dependencies with `uv sync`.
- Register the uv environment as a Jupyter kernel (see `docs/quickstart.md`).
- Copy `.env.example` to `.env` and add SQL Server plus Gemini credentials.

## Directory highlights
- `src/quarto_mssql_gemini/` – reusable Python package for configuration, data access, and Gemini prompts.
- `examples/` – one folder per deliverable with its own README and `outputs/` workspace.
- `assets/` – shared media (PowerPoint template, logos).
- `scripts/` – helpers for running the right `quarto render` command.
- `docs/` – extended guides: quick start, architecture, and how to extend the project.

## Pick an example
| Example | Output | How to render |
| --- | --- | --- |
| Sales dashboard | HTML (`examples/sales-dashboard/outputs/sales-dashboard.html`) | `uv run python scripts/render_dashboard.py` |
| PDF briefing | Typst PDF | `uv run quarto render examples/pdf-briefing/pdf-briefing.qmd` |
| Extended PDF | Typst PDF with extra charts | `uv run quarto render examples/pdf-briefing-extended/pdf-briefing-extended.qmd` |
| Extended PDF (Altair) | Typst PDF + exported PNGs | `uv run quarto render examples/pdf-briefing-extended-altair/pdf-briefing-extended-altair.qmd` |
| PowerPoint deck | PPTX | `uv run quarto render examples/ppt-deck/ppt-deck.qmd --to pptx` |

Each example README describes what you will learn, where outputs land, and how to clean up.

## Helper scripts
- `scripts/render_dashboard.py` – renders the HTML dashboard (good smoke test).
- `scripts/render_all.sh` – rebuilds every example in one go (`uv run bash scripts/render_all.sh`).

## Use the helpers elsewhere
The Python code lives in a `src/` layout. After `uv sync`, import it from anywhere inside the environment:
```python
from quarto_mssql_gemini.data_access import get_germany_sales_data
```
Adapt the helpers or add new prompts in `src/quarto_mssql_gemini/ai/`, then reference them from your own notebooks or Quarto documents.
