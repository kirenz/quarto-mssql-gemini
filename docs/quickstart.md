# Quick Start

Follow these steps to get the demos running with a fresh environment:

1. Open the integrated terminal in VS Code 

2. **Register the uv interpreter as a Jupyter kernel** (required for Quarto to pick it up):
   ```bash
   uv run python -m ipykernel install --user --name quarto-mssql-gemini --display-name "quarto-mssql-gemini"
   ```

3. **Verify the database connection**
   ```bash
   uv run python -c "from quarto_mssql_gemini.data_access import get_germany_sales_data; print(get_germany_sales_data().head())"
   ```
4. **Render your first asset**
   ```bash
   uv run python scripts/render_dashboard.py --open
   ```
   The resulting HTML lives at `examples/sales-dashboard/outputs/sales-dashboard.html`. Drop the `--open` flag if you prefer to skip launching a browser.

Once everything works, explore the other examples inside the `examples/` folder or run the batch renderer:

```bash
uv run bash scripts/render_all.sh
```
