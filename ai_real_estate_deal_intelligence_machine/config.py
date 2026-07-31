from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


# ============================================================
# Application Paths
# ============================================================

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = WORKSPACE_ROOT / "data"

DATA_DIR.mkdir(
    exist_ok=True
)

DB_PATH = DATA_DIR / "phase0.db"

AUDIT_LOG_PATH = DATA_DIR / "audit.log"


# ============================================================
# Environment Helpers
# ============================================================

def env_bool(
    name: str,
    default: bool = False,
) -> bool:
    """
    Convert environment variable to boolean safely.
    """

    value = os.getenv(name)

    if value is None:
        return default

    return value.lower() in {
        "true",
        "1",
        "yes",
        "on",
    }



def env_int(
    name: str,
    default: int,
) -> int:
    """
    Convert environment variable to integer safely.
    """

    value = os.getenv(name)

    if value is None:
        return default

    return int(value)


# ============================================================
# SaaS Application Settings
# ============================================================

@dataclass(
    frozen=True
)
class Settings:
    """
    Central production configuration.

    All runtime services should read from this object.
    """

    # Application
    app_name: str = os.getenv(
        "APP_NAME",
        "AI Real Estate Deal Intelligence Machine",
    )

    app_version: str = os.getenv(
        "APP_VERSION",
        "1.0.0",
    )


    # Environment
    app_env: str = os.getenv(
        "APP_ENV",
        "development",
    )


    # Security
    secret_key: str = os.getenv(
        "SECRET_KEY",
        "development-secret-change-me",
    )


    # Database
    database_url: str = os.getenv(
        "DATABASE_URL",
        f"sqlite:///{DB_PATH}",
    )


    # AI Runtime Modes
    mock_provider_mode: bool = env_bool(
        "MOCK_PROVIDER_MODE",
        True,
    )


    autonomy_mode: str = os.getenv(
        "AUTONOMY_MODE",
        "supervised",
    )


    # Logging
    log_level: str = os.getenv(
        "LOG_LEVEL",
        "INFO",
    )


    audit_log_path: str = os.getenv(
        "AUDIT_LOG_PATH",
        str(AUDIT_LOG_PATH),
    )


    # Job Processing
    stale_job_timeout_seconds: int = env_int(
        "STALE_JOB_TIMEOUT_SECONDS",
        3600,
    )

    # Backward compatibility for existing runtime modules
    # and production bootstrap code.
    STALE_JOB_TIMEOUT_SECONDS: int = stale_job_timeout_seconds


    # API
    api_host: str = os.getenv(
        "API_HOST",
        "0.0.0.0",
    )


    api_port: int = env_int(
        "API_PORT",
        8000,
    )


    # SaaS Features
    enable_live_providers: bool = env_bool(
        "ENABLE_LIVE_PROVIDERS",
        False,
    )


    enable_billing: bool = env_bool(
        "ENABLE_BILLING",
        False,
    )


# ============================================================
# Global Settings Instance
# ============================================================

settings = Settings()