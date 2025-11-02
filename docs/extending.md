# Extending the Project

## Swap in a different region or dataset
- Update `get_germany_sales_data()` or create a sibling helper (e.g. `get_country_sales_data(country)`).
- Adjust your example to import the new helper and regenerate the output.

## Customise Gemini prompts
- Short captions live in `quarto_mssql_gemini.ai.captions.generate_chart_caption`.
- Longer narratives use `quarto_mssql_gemini.ai.narrative.generate_sales_narrative`.
- Modify prompt text or add new helper functions, then import them inside your Quarto document.

## Manage secrets safely
- Store credentials in `.env` and never commit real values.
- The helpers raise a `ConfigurationError` when required variables are missing, giving quick feedback during renders.

## Package and reuse the helpers
- The project uses a `src/` layout with setuptools metadata, so `uv sync` installs the package as `quarto_mssql_gemini`.
- From any script in the environment you can import the helpers directly:
  ```python
  from quarto_mssql_gemini.data_access import get_germany_sales_data
  ```

## Contribute new examples
1. Copy an existing folder under `examples/` as a template.
2. Add a concise README and keep outputs inside the nested `outputs/` directory.
3. Update `scripts/render_all.sh` if you want the new example included in the batch renderer.
4. Document the change in the main README so beginners can discover it.
