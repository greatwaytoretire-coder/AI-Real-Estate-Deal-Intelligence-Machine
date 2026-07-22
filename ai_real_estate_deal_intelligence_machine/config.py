from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    app_env: str = os.getenv("APP_ENV", "development")
    mock_provider_mode: bool = os.getenv("MOCK_PROVIDER_MODE", "true").lower() == "true"
    autonomy_mode: str = os.getenv("AUTONOMY_MODE", "supervised")
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./data/phase0.db")
    audit_log_path: str = os.getenv("AUDIT_LOG_PATH", "./data/audit.log")


settings = Settings()

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = WORKSPACE_ROOT / "data"
DB_PATH = DATA_DIR / "phase0.db"
AUDIT_LOG_PATH = DATA_DIR / "audit.log"
