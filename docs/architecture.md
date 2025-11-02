# Architecture Overview

```
quarto-mssql-gemini/
├─ src/quarto_mssql_gemini/
│  ├─ config.py          # Environment parsing and validation
│  ├─ data_access.py     # SQL Server helpers
│  └─ ai/
│     ├─ narrative.py    # Gemini narratives (2–4 sentence summaries)
│     └─ captions.py     # Short chart captions
├─ examples/
│  ├─ sales-dashboard/
│  ├─ pdf-briefing/
│  ├─ pdf-briefing-extended/
│  ├─ pdf-briefing-extended-altair/
│  └─ ppt-deck/
├─ assets/              # Shared media (PPT template, logos, etc.)
├─ scripts/             # Convenience wrappers around `quarto render`
└─ docs/                # Onboarding and contributor guides
```

## Data flow
1. `quarto_mssql_gemini.data_access.get_germany_sales_data()` builds a SQLAlchemy engine from the environment and fetches Germany-specific rows.
2. Notebooks/examples operate on the returned pandas `DataFrame` and prepare aggregations.
3. Narrative/caption prompts call Gemini using the helpers in `quarto_mssql_gemini.ai.*`.
4. Quarto renders the final output (HTML, PDF, PPTX) per example.

## Adding a new example
- Create a folder under `examples/` with an `outputs/` subdirectory (gitignored).
- Reference shared Python utilities via `from quarto_mssql_gemini ...`.
- Place any reusable media in `assets/` rather than the example folder.
- Document the workflow in a local `README.md` to guide newcomers.
