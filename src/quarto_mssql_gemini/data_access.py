"""Database connectivity helpers."""

from __future__ import annotations

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import URL, Engine

from .config import DatabaseSettings, ConfigurationError, get_database_settings


GERMANY_SALES_QUERY = """
SELECT [Sales Organisation], [Sales Country], [Sales Region], [Sales City],
       [Product Line], [Product Category], [Calendar Year], [Calendar Quarter],
       [Calendar Month], [Calendar DueDate], [Sales Amount], [Revenue EUR],
       [Revenue Quota], [Gross Profit EUR], [Gross Profit Quota], [Discount EUR]
FROM [DataSet_Monthly_Sales_and_Quota]
WHERE [Sales Country] = 'Germany'
"""


def _build_connection_url(settings: DatabaseSettings) -> URL:
    host = settings.server if not settings.port else f"{settings.server},{settings.port}"

    query_params = {
        "driver": settings.driver,
        "TrustServerCertificate": "yes" if settings.trust_server_certificate else "no",
    }
    if settings.odbc_extra:
        query_params.update(settings.odbc_extra)

    return URL.create(
        "mssql+pyodbc",
        username=settings.username,
        password=settings.password,
        host=host,
        database=settings.database,
        query=query_params,
    )


def get_database_engine() -> Engine:
    """Create a SQLAlchemy engine using environment-backed settings."""

    settings = get_database_settings()
    try:
        return create_engine(_build_connection_url(settings))
    except Exception as exc:  # pragma: no cover - surface friendly message to notebooks
        raise ConfigurationError(f"Failed to create database engine: {exc}") from exc


def get_germany_sales_data() -> pd.DataFrame:
    """Retrieve the Germany slice of monthly sales and quota data."""

    engine = get_database_engine()
    try:
        df = pd.read_sql(GERMANY_SALES_QUERY, engine)
    finally:
        engine.dispose()

    df["Calendar DueDate"] = pd.to_datetime(df["Calendar DueDate"])
    return df
