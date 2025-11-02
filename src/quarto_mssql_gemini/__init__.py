"""Utilities for combining SQL Server data with Gemini-powered analysis."""

from .data_access import get_database_engine, get_germany_sales_data
from .ai.narrative import generate_sales_narrative
from .ai.captions import generate_chart_caption

__all__ = [
    "generate_sales_narrative",
    "generate_chart_caption",
    "get_database_engine",
    "get_germany_sales_data",
]
