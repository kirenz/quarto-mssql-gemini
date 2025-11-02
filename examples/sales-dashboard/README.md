# Sales Dashboard

This walkthrough builds the interactive dashboard that combines SQL Server data with Gemini commentary.

## What you'll learn
- Pull the prepared Germany sales data with `quarto_mssql_gemini.data_access`.
- Enrich Altair visuals with short AI captions from `quarto_mssql_gemini.ai.captions`.
- Render a Quarto dashboard and inspect the generated HTML output.

## Run it
1. Configure your `.env` (host, database, credentials, Gemini key). See the project quick start for details.
2. From the repository root, render the notebook:  
   `uv run quarto render examples/sales-dashboard/sales-dashboard.qmd`
3. Open `examples/sales-dashboard/outputs/sales-dashboard.html` in a browser. Supporting assets (CSS/JS) live inside the `sales-dashboard_files/` folder next to the HTML.

## Key files
- `sales-dashboard.qmd` – the Quarto source.
- `outputs/` – regenerated assets; safe to delete and rebuild at any time.
