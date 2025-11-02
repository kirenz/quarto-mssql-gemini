"""Configuration helpers for database and Gemini access."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Dict, Iterable

from dotenv import load_dotenv

load_dotenv()


class ConfigurationError(RuntimeError):
    """Raised when the expected environment cannot be constructed."""


@dataclass
class DatabaseSettings:
    """Resolved configuration for connecting to SQL Server."""

    server: str
    database: str
    username: str
    password: str
    driver: str
    trust_server_certificate: bool
    port: str | None = None
    odbc_extra: Dict[str, str] | None = None


DEFAULT_DRIVER_PATH = "/opt/homebrew/lib/libmsodbcsql.17.dylib"


def _collect_required(names: Iterable[str]) -> Dict[str, str]:
    missing = [name for name in names if not os.getenv(name)]
    if missing:
        joined = ", ".join(sorted(missing))
        raise ConfigurationError(
            "Missing required environment variables: "
            f"{joined}. Update your .env file before rendering."
        )
    return {name: os.getenv(name, "") for name in names}


def get_database_settings() -> DatabaseSettings:
    """Resolve the SQL Server credentials from environment variables."""

    env = _collect_required(("MSSQL_SERVER", "MSSQL_DATABASE", "MSSQL_USERNAME", "MSSQL_PASSWORD"))

    driver = os.getenv("MSSQL_DRIVER") or DEFAULT_DRIVER_PATH
    trust_raw = os.getenv("TRUST_SERVER_CERTIFICATE", "false")
    trust_flag = trust_raw.lower() in {"1", "true", "yes", "on"}

    port = os.getenv("MSSQL_PORT")

    odbc_extra_env = os.getenv("MSSQL_ODBC_EXTRA", "")
    odbc_extra: Dict[str, str] | None = None
    if odbc_extra_env:
        pairs = [segment.strip() for segment in odbc_extra_env.split(";") if segment.strip()]
        if pairs:
            odbc_extra = {}
            for pair in pairs:
                if "=" in pair:
                    key, value = pair.split("=", 1)
                    odbc_extra[key.strip()] = value.strip()

    return DatabaseSettings(
        server=env["MSSQL_SERVER"],
        database=env["MSSQL_DATABASE"],
        username=env["MSSQL_USERNAME"],
        password=env["MSSQL_PASSWORD"],
        driver=driver,
        trust_server_certificate=trust_flag,
        port=port,
        odbc_extra=odbc_extra,
    )


def get_gemini_api_key() -> str:
    """Fetch the Gemini API key from the environment, raising if absent."""

    key = os.getenv("GEMINI_API_KEY")
    if not key:
        raise ConfigurationError(
            "Missing required environment variable: GEMINI_API_KEY. "
            "Set it in your .env file to enable Gemini-powered analysis."
        )
    return key
