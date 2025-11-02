# Quarto MSSQL Gemini Starter

Ready-to-share Quarto examples that combine Microsoft SQL Server data with Gemini-generated commentary. 

Quarto is used to author HTML dashboards, PDF briefings, and PowerPoint decks. The Gemini API generates narrative text based on data queried from MSSQL.

## Prerequisites

This project assumes you have already installed:

- [uv](https://github.com/astral-sh/uv)
- An ODBC driver for SQL Server (see this [installation guide](https://kirenz.github.io/database-mssql/))

## Quick start

1. Install [uv](https://github.com/astral-sh/uv), follow the [Quarto installation guide](https://quarto.org/docs/get-started/), and an ODBC driver for SQL Server.

2. Clone the toolkit:
```bash
git clone https://github.com/kirenz/quarto-mssql-gemini.git
```

3. Enter the project folder:
```bash
cd quarto-mssql-gemini
```

4. Install dependencies:
```bash
uv sync
```

5. Copy the environment template and create your own `.env` file:

```bash
cp .env.example .env
```

6. Open VS Code in the project folder

```bash
code .
```

7. Edit `.env` to add MSSQL credentials and `GEMINI_API_KEY`.


8. Open the [quick start guide](docs/quickstart.md) and follow the steps to render your first asset.


## Directory highlights
- `src/quarto_mssql_gemini/` – reusable Python package for configuration, data access, and Gemini prompts.
- `examples/` – one folder per deliverable with its own README and `outputs/` workspace.
- `assets/` – shared media (PowerPoint template, logos).
- `scripts/` – helpers for running the right `quarto render` command.
- `docs/` – extended guides: quick start, architecture, and how to extend the project.

## Pick an example
| Example | Output | How to render |
| --- | --- | --- |
| Sales dashboard | HTML (`examples/sales-dashboard/outputs/sales-dashboard.html`) | `uv run python scripts/render_dashboard.py`<br/>Add `--open` to launch the page in your browser. |
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
