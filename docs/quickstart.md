# Quick Start

Follow these steps to get the demos running with a fresh environment:

1. **Install dependencies**
   ```bash
   uv sync
   ```
2. **Register the uv interpreter as a Jupyter kernel** (required for Quarto to pick it up):
   ```bash
   uv run python -m ipykernel install --user --name quarto-mssql-gemini --display-name "quarto-mssql-gemini"
   ```
3. **Copy the environment template and fill in credentials**
   ```bash
   cp .env.example .env
   ```
   Populate SQL Server settings (`MSSQL_*`) and your Gemini key.
4. **Verify the database connection**
   ```bash
   uv run python -c "from quarto_mssql_gemini.data_access import get_germany_sales_data; print(get_germany_sales_data().head())"
   ```
5. **Render your first asset**
   ```bash
   uv run python scripts/render_dashboard.py
   ```
   The resulting HTML lives at `examples/sales-dashboard/outputs/sales-dashboard.html`.

Once everything works, explore the other examples inside the `examples/` folder or run the batch renderer:
```bash
uv run bash scripts/render_all.sh
```
