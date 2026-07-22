from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from .config import AUDIT_LOG_PATH


class AuditLogger:
    """Phase 0 audit logger writing to a local file for traceability."""

    def __init__(self, log_path: Path = AUDIT_LOG_PATH) -> None:
        self.log_path = Path(log_path)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

    def log(self, event_type: str, details: str) -> None:
        timestamp = datetime.now(timezone.utc).isoformat()
        payload = f"[{timestamp}] {event_type} | {details}\n"
        with self.log_path.open("a", encoding="utf-8") as handle:
            handle.write(payload)
