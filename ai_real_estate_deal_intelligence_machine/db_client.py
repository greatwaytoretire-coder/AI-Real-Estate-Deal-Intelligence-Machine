from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional

from .config import DB_PATH, DATA_DIR


class DatabaseClient:
    """Minimal local SQLite client for Phase 0.

    This is intentionally lightweight and uses only local infrastructure so the
    system remains zero-budget during the foundational phase.
    """

    def __init__(self, database_path: Path = DB_PATH) -> None:
        self.database_path = Path(database_path)
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        self._connection = sqlite3.connect(self.database_path)
        self._connection.row_factory = sqlite3.Row
        self.initialize()

    def initialize(self) -> None:
        schema = """
        CREATE TABLE IF NOT EXISTS providers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            label TEXT NOT NULL,
            source_type TEXT NOT NULL,
            enabled INTEGER NOT NULL DEFAULT 1
        );

        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            organization_id TEXT NOT NULL,
            event_type TEXT NOT NULL,
            details TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS integration_stages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            stage TEXT NOT NULL,
            payload TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS contact_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            organization_id TEXT NOT NULL,
            entity_id TEXT NOT NULL,
            action_id TEXT,
            status TEXT,
            contact_timestamp TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS contact_preferences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            organization_id TEXT NOT NULL,
            entity_id TEXT NOT NULL,
            has_opted_out INTEGER NOT NULL DEFAULT 0,
            updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(organization_id, entity_id)
        );

        CREATE TABLE IF NOT EXISTS organizations (
            organization_id TEXT PRIMARY KEY,
            name TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            organization_id TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            hashed_password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'member',
            FOREIGN KEY (organization_id) REFERENCES organizations (organization_id)
        );

        CREATE TABLE IF NOT EXISTS schema_version (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            version INTEGER NOT NULL
        );
        INSERT OR IGNORE INTO schema_version (id, version) VALUES (1, 1);
        """
        with self._connection:
            self._connection.executescript(schema)

    def upsert_provider(self, name: str, label: str, source_type: str = "mock") -> None:
        with self._connection:
            self._connection.execute(
                """
                INSERT INTO providers (name, label, source_type, enabled)
                VALUES (?, ?, ?, 1)
                ON CONFLICT(name) DO UPDATE SET
                    label = excluded.label,
                    source_type = excluded.source_type,
                    enabled = 1
                """,
                (name, label, source_type),
            )

    def list_providers(self) -> List[Dict[str, Any]]:
        cursor = self._connection.execute(
            "SELECT name, label, source_type, enabled FROM providers ORDER BY id"
        )
        return [dict(row) for row in cursor.fetchall()]

    def log_audit(self, organization_id: str, event_type: str, details: str) -> None:
        with self._connection:
            self._connection.execute(
                "INSERT INTO audit_logs (organization_id, event_type, details) VALUES (?, ?, ?)",
                (organization_id, event_type, details),
            )

    def list_audit_logs(self, organization_id: str) -> List[Dict[str, Any]]:
        cursor = self._connection.execute(
            "SELECT id, event_type, details, created_at FROM audit_logs WHERE organization_id = ? ORDER BY id",
            (organization_id,),
        )
        return [dict(row) for row in cursor.fetchall()]

    def record_stage_result(self, stage: str, payload: Dict[str, Any]) -> None:
        # This table is for system-wide integration tests, not tenant data, so it remains global.
        with self._connection:
            self._connection.execute(
                "INSERT INTO integration_stages (stage, payload) VALUES (?, ?)",
                (stage, json.dumps(payload)),
            )

    def list_stage_results(self) -> List[Dict[str, Any]]:
        cursor = self._connection.execute(
            "SELECT id, stage, payload, created_at FROM integration_stages ORDER BY id"
        )
        rows = []
        for row in cursor.fetchall():
            payload = json.loads(row["payload"])
            rows.append({"id": row["id"], "stage": row["stage"], "payload": payload, "created_at": row["created_at"]})
        return rows

    def close(self) -> None:
        self._connection.close()
