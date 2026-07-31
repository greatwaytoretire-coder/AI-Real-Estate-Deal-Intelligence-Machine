from __future__ import annotations

import json
import sqlite3

from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

from .config import DB_PATH, DATA_DIR
from .jobs.base import Job, JobStatus


class DatabaseClient:
    """
    SQLite database client.

    Handles:
    - Providers
    - Audit logs
    - Organizations
    - Users
    - Jobs
    - Deduplication
    - Properties
    - Integration records
    """

    def __init__(self, database_path: Path = DB_PATH) -> None:
        self.database_path = Path(database_path)

        DATA_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._connection = sqlite3.connect(
            self.database_path
        )

        self._connection.row_factory = sqlite3.Row

        self.initialize()


    def initialize(self) -> None:
        """
        Creates required database tables.
        """

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
            organization_id TEXT,
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

            UNIQUE(
                organization_id,
                entity_id
            )
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

            FOREIGN KEY(
                organization_id
            )
            REFERENCES organizations(
                organization_id
            )
        );


        CREATE TABLE IF NOT EXISTS schema_version (
            id INTEGER PRIMARY KEY CHECK(id = 1),
            version INTEGER NOT NULL
        );


        INSERT OR IGNORE INTO schema_version
        (
            id,
            version
        )
        VALUES
        (
            1,
            1
        );


        CREATE TABLE IF NOT EXISTS jobs (
            job_id TEXT PRIMARY KEY,
            status TEXT NOT NULL,
            attempts INTEGER NOT NULL DEFAULT 0,
            payload TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );


        CREATE INDEX IF NOT EXISTS idx_jobs_status
        ON jobs(status);



        CREATE TABLE IF NOT EXISTS processed_fingerprints (

            fingerprint TEXT NOT NULL,
            market_id TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

            PRIMARY KEY(
                fingerprint,
                market_id
            )
        );



        CREATE TABLE IF NOT EXISTS properties (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            canonical_id TEXT NOT NULL UNIQUE,

            market_id TEXT NOT NULL,

            address TEXT,
            city TEXT,
            state TEXT,
            zip_code TEXT,

            property_type TEXT,

            bedrooms INTEGER,
            bathrooms REAL,

            square_feet INTEGER,

            estimated_value REAL,

            source TEXT,

            raw_data TEXT NOT NULL,

            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

            updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );


        CREATE INDEX IF NOT EXISTS idx_properties_market
        ON properties(market_id);


        CREATE INDEX IF NOT EXISTS idx_properties_canonical
        ON properties(canonical_id);

        """

        with self._connection:

            self._connection.executescript(
                schema
            )

            self._run_migrations()



    def _run_migrations(self) -> None:
        """
        Applies safe schema updates.
        """

        cursor = self._connection.execute(
            "PRAGMA table_info(audit_logs)"
        )

        columns = [
            row["name"]
            for row in cursor.fetchall()
        ]


        if "organization_id" not in columns:

            self._connection.execute(
                """
                ALTER TABLE audit_logs
                ADD COLUMN organization_id TEXT
                """
            )
    def upsert_provider(
        self,
        name: str,
        label: str,
        source_type: str = "mock",
    ) -> None:

        with self._connection:

            self._connection.execute(
                """
                INSERT INTO providers
                (
                    name,
                    label,
                    source_type,
                    enabled
                )

                VALUES
                (?, ?, ?, 1)

                ON CONFLICT(name)
                DO UPDATE SET

                    label = excluded.label,

                    source_type = excluded.source_type,

                    enabled = 1
                """,

                (
                    name,
                    label,
                    source_type,
                ),
            )



    def list_providers(self) -> List[Dict[str, Any]]:

        cursor = self._connection.execute(
            """
            SELECT
                name,
                label,
                source_type,
                enabled

            FROM providers

            ORDER BY id
            """
        )

        return [
            dict(row)
            for row in cursor.fetchall()
        ]



    def log_audit(
        self,
        event_type: str,
        details: str,
        organization_id: str | None = None,
    ) -> None:

        with self._connection:

            self._connection.execute(
                """
                INSERT INTO audit_logs
                (
                    organization_id,
                    event_type,
                    details
                )

                VALUES
                (?, ?, ?)
                """,

                (
                    organization_id or "system",
                    event_type,
                    details,
                ),
            )



    def list_audit_logs(
        self,
        organization_id: Optional[str] = None,
    ) -> List[Dict[str, Any]]:

        cursor = self._connection.execute(
            """
            SELECT
                id,
                event_type,
                details,
                created_at,
                organization_id

            FROM audit_logs

            WHERE
                (?1 IS NULL
                OR organization_id = ?1)

            ORDER BY id
            """,

            (
                organization_id,
            ),
        )

        return [
            dict(row)
            for row in cursor.fetchall()
        ]



    def record_stage_result(
        self,
        stage: str,
        payload: Dict[str, Any],
    ) -> None:

        with self._connection:

            self._connection.execute(
                """
                INSERT INTO integration_stages
                (
                    stage,
                    payload
                )

                VALUES
                (?, ?)
                """,

                (
                    stage,
                    json.dumps(payload),
                ),
            )



    def list_stage_results(
        self,
    ) -> List[Dict[str, Any]]:

        cursor = self._connection.execute(
            """
            SELECT
                id,
                stage,
                payload,
                created_at

            FROM integration_stages

            ORDER BY id
            """
        )

        results = []

        for row in cursor.fetchall():

            results.append(
                {
                    "id": row["id"],
                    "stage": row["stage"],
                    "payload": json.loads(
                        row["payload"]
                    ),
                    "created_at": row["created_at"],
                }
            )

        return results



    # ==========================================================
    # PROPERTY STORAGE
    # ==========================================================


    def upsert_property(
        self,
        property_data: Dict[str, Any],
    ) -> None:

        """
        Stores discovered property intelligence.
        """

        with self._connection:

            self._connection.execute(
                """
                INSERT INTO properties
                (
                    canonical_id,
                    market_id,
                    address,
                    city,
                    state,
                    zip_code,
                    property_type,
                    bedrooms,
                    bathrooms,
                    square_feet,
                    estimated_value,
                    source,
                    raw_data,
                    updated_at
                )

                VALUES
                (
                    ?, ?, ?, ?, ?,
                    ?, ?, ?, ?, ?,
                    ?, ?, ?, ?
                )


                ON CONFLICT(canonical_id)

                DO UPDATE SET

                    market_id = excluded.market_id,

                    address = excluded.address,

                    city = excluded.city,

                    state = excluded.state,

                    zip_code = excluded.zip_code,

                    property_type = excluded.property_type,

                    bedrooms = excluded.bedrooms,

                    bathrooms = excluded.bathrooms,

                    square_feet = excluded.square_feet,

                    estimated_value = excluded.estimated_value,

                    source = excluded.source,

                    raw_data = excluded.raw_data,

                    updated_at = excluded.updated_at

                """,

                (
                    property_data.get("canonical_id"),

                    property_data.get("market_id"),

                    property_data.get("address"),

                    property_data.get("city"),

                    property_data.get("state"),

                    property_data.get("zip_code"),

                    property_data.get("property_type"),

                    property_data.get("bedrooms"),

                    property_data.get("bathrooms"),

                    property_data.get("square_feet"),

                    property_data.get("estimated_value"),

                    property_data.get("source"),

                    json.dumps(property_data),

                    datetime.now(
                        timezone.utc
                    ).isoformat(),
                ),
            )



    def list_properties(
        self,
    ) -> List[Dict[str, Any]]:

        cursor = self._connection.execute(
            """
            SELECT *

            FROM properties

            ORDER BY id DESC
            """
        )

        return [
            dict(row)
            for row in cursor.fetchall()
        ]



    # ==========================================================
    # JOB MANAGEMENT
    # ==========================================================


    def create_job(
        self,
        job: Job,
    ) -> None:

        with self._connection:

            self._connection.execute(
                """
                INSERT INTO jobs
                (
                    job_id,
                    status,
                    attempts,
                    payload,
                    updated_at
                )

                VALUES
                (?, ?, ?, ?, ?)

                """,

                (
                    job.job_id,

                    job.status.value,

                    job.attempts,

                    json.dumps(
                        job.payload
                    ),

                    datetime.now(
                        timezone.utc
                    ).isoformat(),

                ),
            )
    def update_job_status(
        self,
        job_id: str,
        status: JobStatus,
        attempts: Optional[int] = None,
    ) -> None:

        with self._connection:

            if attempts is not None:

                self._connection.execute(
                    """
                    UPDATE jobs

                    SET
                        status = ?,
                        attempts = ?,
                        updated_at = ?

                    WHERE job_id = ?
                    """,

                    (
                        status.value,

                        attempts,

                        datetime.now(
                            timezone.utc
                        ).isoformat(),

                        job_id,
                    ),
                )

            else:

                self._connection.execute(
                    """
                    UPDATE jobs

                    SET
                        status = ?,
                        updated_at = ?

                    WHERE job_id = ?
                    """,

                    (
                        status.value,

                        datetime.now(
                            timezone.utc
                        ).isoformat(),

                        job_id,
                    ),
                )



    def get_pending_job_id(
        self,
    ) -> Optional[str]:

        cursor = self._connection.execute(
            """
            SELECT job_id

            FROM jobs

            WHERE status IN (?, ?)

            ORDER BY created_at ASC

            LIMIT 1
            """,

            (
                JobStatus.PENDING.value,

                JobStatus.RETRY_SCHEDULED.value,
            ),
        )

        row = cursor.fetchone()

        return row["job_id"] if row else None



    def get_job(
        self,
        job_id: str,
    ) -> Optional[Job]:

        cursor = self._connection.execute(
            """
            SELECT *

            FROM jobs

            WHERE job_id = ?
            """,

            (
                job_id,
            ),
        )

        row = cursor.fetchone()

        if not row:
            return None


        return Job(
            job_id=row["job_id"],

            status=JobStatus(
                row["status"]
            ),

            attempts=row["attempts"],

            payload=json.loads(
                row["payload"]
            ),
        )



    def list_jobs_by_status(
        self,
        status: JobStatus,
    ) -> List[Job]:

        cursor = self._connection.execute(
            """
            SELECT *

            FROM jobs

            WHERE status = ?
            """,

            (
                status.value,
            ),
        )


        return [

            Job(
                job_id=row["job_id"],

                status=JobStatus(
                    row["status"]
                ),

                attempts=row["attempts"],

                payload=json.loads(
                    row["payload"]
                ),
            )

            for row in cursor.fetchall()

        ]



    # ==========================================================
    # DEDUPLICATION
    # ==========================================================


    def add_fingerprint(
        self,
        fingerprint: str,
        market_id: str,
    ) -> None:

        with self._connection:

            self._connection.execute(
                """
                INSERT OR IGNORE INTO processed_fingerprints

                (
                    fingerprint,
                    market_id
                )

                VALUES
                (?, ?)

                """,

                (
                    fingerprint,

                    market_id,
                ),
            )



    def has_fingerprint(
        self,
        fingerprint: str,
        market_id: str,
    ) -> bool:

        cursor = self._connection.execute(
            """
            SELECT 1

            FROM processed_fingerprints

            WHERE
                fingerprint = ?

            AND
                market_id = ?

            """,

            (
                fingerprint,

                market_id,
            ),
        )


        return cursor.fetchone() is not None



    def recover_stale_running_jobs(
        self,
        stale_after_seconds: int,
    ) -> int:

        stale_threshold = (
            datetime.now(timezone.utc)
            -
            timedelta(
                seconds=stale_after_seconds
            )
        )


        with self._connection:

            cursor = self._connection.execute(
                """
                UPDATE jobs

                SET

                    status = ?,

                    updated_at = ?

                WHERE

                    status = ?

                AND

                    updated_at < ?

                """,

                (

                    JobStatus.RETRY_SCHEDULED.value,

                    datetime.now(
                        timezone.utc
                    ).isoformat(),

                    JobStatus.RUNNING.value,

                    stale_threshold.isoformat(),

                ),
            )


            return cursor.rowcount



    # ==========================================================
    # USER MANAGEMENT
    # ==========================================================


    def create_user(
        self,
        user: Any,
    ) -> None:

        with self._connection:

            self._connection.execute(
                """
                INSERT INTO users

                (
                    user_id,
                    organization_id,
                    email,
                    hashed_password,
                    role
                )

                VALUES
                (?, ?, ?, ?, ?)

                """,

                (

                    user.user_id,

                    user.organization_id,

                    user.email,

                    user.hashed_password,

                    user.role,

                ),
            )



    def find_user_by_email(
        self,
        email: str,
    ) -> Optional[Dict[str, Any]]:

        cursor = self._connection.execute(
            """
            SELECT

                user_id,

                organization_id,

                email,

                hashed_password,

                role

            FROM users

            WHERE email = ?

            """,

            (
                email,
            ),
        )


        row = cursor.fetchone()


        return dict(row) if row else None



    # ==========================================================
    # CONNECTION MANAGEMENT
    # ==========================================================


    def close(
        self,
    ) -> None:

        self._connection.close()



    def __enter__(
        self,
    ) -> "DatabaseClient":

        return self



    def __exit__(
        self,
        exc_type,
        exc_val,
        exc_tb,
    ) -> None:

        self.close()