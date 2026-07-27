from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, Set
from uuid import uuid4

from .audit_logger import AuditLogger
from .phase26 import ProviderManager
from .phase29 import MarketStatus, ScalingManager
from .runtime.base import IngestionRun
from .jobs.base import Job, JobStatus

class OperatingMode(str, Enum):
    """Defines the operating mode of the system."""
    DEVELOPMENT = "development"
    MOCK = "mock"
    PILOT = "pilot"

@dataclass
class CanonicalProperty:
    """A normalized internal representation of a property."""
    canonical_id: str
    source_provider: str
    source_record_id: str
    address: str
    zip_code: str
    fingerprint: str

@dataclass
class RuntimeEvent:
    """A durable event representing a state change."""
    event_id: str = field(
        default_factory=lambda: f"evt_{uuid4()}"
    )
    event_type: str = "GENERIC_EVENT"
    entity_id: str = ""
    payload_ref: str = ""
    status: str = "PENDING"

class SystemState:
    """Tracks basic runtime state."""
    def __init__(
        self,
        audit_logger: AuditLogger,
    ) -> None:
        self.audit_logger = audit_logger
        self.processed_ids: Set[str] = set()
        self.failed_ids: Set[str] = set()
        self.runtime_events: List[RuntimeEvent] = []

    def record_event(
        self,
        event_type: str,
        entity_id: str = "",
        payload_ref: str = "",
    ) -> RuntimeEvent:
        """Records a runtime event."""
        event = RuntimeEvent(
            event_type=event_type,
            entity_id=entity_id,
            payload_ref=payload_ref,
        )
        self.runtime_events.append(event)
        return event

class ReliabilityEngine:
    """Handles retry and reliability tracking for runtime jobs."""
    def __init__(
        self,
        system_state: SystemState,
        max_retries: int = 3,
    ) -> None:
        self.system_state = system_state
        self.max_retries = max_retries
        self.processed_ids: Set[str] = set()

    def mark_processed(
        self,
        job_id: str,
    ) -> None:
        """Marks a job as successfully processed."""
        self.processed_ids.add(job_id)
        self.system_state.processed_ids.add(job_id)

    def mark_failed(
        self,
        job_id: str,
    ) -> None:
        """Marks a job as failed."""
        self.system_state.failed_ids.add(job_id)

class DeduplicationEngine:
    """Prevents duplicate records from being processed."""
    def __init__(self) -> None:
        self.processed_fingerprints: Dict[
            str,
            Set[str],
        ] = {}

    def is_duplicate(
        self,
        fingerprint: str,
        market_id: str,
    ) -> bool:
        """Checks whether a fingerprint was already processed."""
        return fingerprint in self.processed_fingerprints.get(
            market_id,
            set(),
        )

    def add(
        self,
        fingerprint: str,
        market_id: str,
    ) -> None:
        """Adds a fingerprint to a market's processed set."""
        self.processed_fingerprints.setdefault(
            market_id,
            set(),
        ).add(fingerprint)

class NormalizationEngine:
    """Converts raw provider data into canonical internal data."""
    def normalize_property(
        self,
        raw_data: Dict[str, Any],
    ) -> CanonicalProperty:
        """Normalizes a raw property record."""
        address = str(raw_data.get("address", "")).strip()
        zip_code = str(raw_data.get("zip", "")).strip()

        fingerprint = hashlib.sha256(
            f"{address}|{zip_code}".encode()
        ).hexdigest()

        return CanonicalProperty(
            canonical_id=f"prop_{uuid4()}",
            source_provider=str(
                raw_data.get(
                    "provider",
                    "unknown",
                )
            ),
            source_record_id=str(
                raw_data.get(
                    "id",
                    uuid4(),
                )
            ),
            address=address,
            zip_code=zip_code,
            fingerprint=fingerprint,
        )

class RuntimeJobQueue:
    """A durable in-memory job queue."""
    def __init__(self) -> None:
        self.jobs: Dict[str, Job] = {}
        self.pending_queue: List[str] = []
        self.dead_letter_queue: List[Job] = []

    def submit_job(
        self,
        job: Job,
    ) -> bool:
        """Adds a job if it has not already been submitted."""
        if job.job_id in self.jobs:
            return False

        self.jobs[job.job_id] = job
        self.pending_queue.append(job.job_id)

        return True

    def get_pending_job(
        self,
    ) -> Optional[Job]:
        """Returns the next pending job."""
        if not self.pending_queue:
            return None

        job_id = self.pending_queue.pop(0)
        job = self.jobs.get(job_id)

        if job is not None:
            job.status = JobStatus.RUNNING

        return job

    def schedule_for_retry(
        self,
        job: Job,
    ) -> None:
        """Schedules a job for another attempt."""
        job.status = JobStatus.RETRY_SCHEDULED
        self.pending_queue.append(job.job_id)

class Worker:
    """Processes jobs from the runtime queue."""
    def __init__(
        self,
        job_queue: RuntimeJobQueue,
        audit_logger: AuditLogger,
        reliability_engine: ReliabilityEngine,
        orchestrator: Any,
        db_client: Optional[Any] = None,
    ) -> None:
        self.job_queue = job_queue
        self.audit_logger = audit_logger
        self.reliability_engine = reliability_engine
        self.orchestrator = orchestrator
        self.db_client = db_client

    def run(
        self,
        failure_simulation: bool = False,
    ) -> None:
        """Picks up and executes one job."""
        job = self.job_queue.get_pending_job()

        if job is None:
            return

        job.attempts += 1

        self.audit_logger.log(
            "WORKER_START",
            (
                f"Worker started processing "
                f"job {job.job_id}."
            ),
        )

        try:
            if failure_simulation:
                raise ValueError(
                    "Simulated AI pipeline failure."
                )

            output = self.orchestrator.handle_job(job)

            error_message = getattr(
                output,
                "error",
                None,
            )

            if error_message:
                raise RuntimeError(
                    f"Orchestration failed: "
                    f"{error_message}"
                )

            job.status = JobStatus.COMPLETED

            if self.db_client is not None:
                update_job_status = getattr(
                    self.db_client,
                    "update_job_status",
                    None,
                )

                if callable(update_job_status):
                    update_job_status(
                        job.job_id,
                        job.status,
                        job.attempts,
                    )

            self.reliability_engine.mark_processed(
                job.job_id
            )

            self.audit_logger.log(
                "WORKER_SUCCESS",
                (
                    f"Job {job.job_id} "
                    "completed successfully."
                ),
            )

        except Exception as error:
            self.audit_logger.log(
                "WORKER_ERROR",
                (
                    f"Job {job.job_id} "
                    f"failed: {error}"
                ),
            )

            self.reliability_engine.mark_failed(
                job.job_id
            )

            if (
                job.attempts
                >= self.reliability_engine.max_retries
            ):
                job.status = JobStatus.DEAD_LETTER

                self.job_queue.dead_letter_queue.append(
                    job
                )

                if self.db_client is not None:
                    update_job_status = getattr(
                        self.db_client,
                        "update_job_status",
                        None,
                    )

                    if callable(update_job_status):
                        update_job_status(
                            job.job_id,
                            job.status,
                            job.attempts,
                        )

                self.audit_logger.log(
                    "RELIABILITY_DLQ",
                    (
                        f"Job {job.job_id} "
                        "moved to DLQ after "
                        f"{job.attempts} attempts."
                    ),
                )

            else:
                self.job_queue.schedule_for_retry(job)

                self.audit_logger.log(
                    "RELIABILITY",
                    (
                        f"Re-queuing job "
                        f"{job.job_id} for attempt "
                        f"{job.attempts + 1}."
                    ),
                )

class ContinuousRuntime:
    """Orchestrates continuous ingestion and processing."""
    def __init__(
        self,
        audit_logger: AuditLogger,
        provider_manager: ProviderManager,
        orchestrator: Any,
        scaling_manager: ScalingManager,
        job_queue: Optional[
            RuntimeJobQueue
        ] = None,
        deduplication_engine: Optional[
            DeduplicationEngine
        ] = None,
    ) -> None:
        self.mode = OperatingMode.DEVELOPMENT

        self.audit_logger = audit_logger
        self.provider_manager = provider_manager
        self.orchestrator = orchestrator
        self.scaling_manager = scaling_manager

        self.system_state = SystemState(
            audit_logger=audit_logger
        )

        self.reliability_engine = ReliabilityEngine(
            system_state=self.system_state
        )

        self.job_queue = (
            job_queue
            if job_queue is not None
            else RuntimeJobQueue()
        )

        self.deduplication_engine = (
            deduplication_engine
            if deduplication_engine is not None
            else DeduplicationEngine()
        )

        self.normalization_engine = NormalizationEngine()

        db_client_for_worker = getattr(
            self.job_queue,
            "db_client",
            None,
        )

        self.worker = Worker(
            job_queue=self.job_queue,
            audit_logger=self.audit_logger,
            reliability_engine=self.reliability_engine,
            orchestrator=self.orchestrator,
            db_client=db_client_for_worker,
        )

        self.raw_data_store: List[
            Dict[str, Any]
        ] = []

        self.canonical_db: Dict[
            str,
            CanonicalProperty,
        ] = {}

    def run_ingestion_for_market(
        self,
        market_id: str,
        query: Dict[str, Any],
    ) -> IngestionRun:
        """Runs a complete ingestion cycle."""
        market_config = (
            self.scaling_manager.get_market_config(
                market_id
            )
        )

        run_log = IngestionRun(
            provider=market_id,
            start_time=datetime.now(
                timezone.utc
            ).isoformat(),
        )

        if (
            market_config is None
            or market_config.status
            != MarketStatus.ACTIVE
        ):
            run_log.errors.append(
                (
                    f"Market '{market_id}' "
                    "is not active or does "
                    "not exist."
                )
            )

            return run_log

        for provider_name in market_config.data_providers:
            provider = (
                self.provider_manager.providers.get(
                    provider_name
                )
            )

            if provider is None:
                run_log.errors.append(
                    (
                        f"Provider "
                        f"'{provider_name}' "
                        f"for market "
                        f"'{market_id}' "
                        "not found."
                    )
                )

                continue

            provider_config = provider.get_config()

            source_type = getattr(
                provider_config,
                "source_type",
                None,
            )

            source_type_value = str(
                getattr(
                    source_type,
                    "value",
                    source_type,
                )
            ).upper()

            if (
                self.mode == OperatingMode.MOCK
                and source_type_value == "LIVE"
            ):
                self.audit_logger.log(
                    "INGESTION_SKIP",
                    (
                        f"Skipping LIVE provider "
                        f"'{provider_name}' "
                        "in MOCK mode."
                    ),
                )

                continue

            try:
                raw_records = provider.fetch(query)

                for raw_record in raw_records:
                    run_log.records_discovered += 1

                    self.raw_data_store.append(
                        raw_record
                    )

                    normalized = (
                        self.normalization_engine
                        .normalize_property(
                            raw_record
                        )
                    )

                    if (
                        self.deduplication_engine
                        .is_duplicate(
                            normalized.fingerprint,
                            market_id,
                        )
                    ):
                        run_log.records_skipped += 1
                        continue

                    self.deduplication_engine.add(
                        normalized.fingerprint,
                        market_id,
                    )

                    self.canonical_db[
                        normalized.canonical_id
                    ] = normalized

                    run_log.records_inserted += 1

                    job = Job(
                        job_id=(
                            f"process_"
                            f"{normalized.canonical_id}"
                        ),
                        payload={
                            "event_type": (
                                "PROPERTY_DISCOVERED"
                            ),
                            "entity_id": (
                                normalized.canonical_id
                            ),
                            "market_id": market_id,
                            "scoring_model_version": (
                                market_config
                                .scoring_model_version
                            ),
                        },
                    )

                    self.job_queue.submit_job(job)

            except Exception as error:
                self.audit_logger.log(
                    "INGESTION_ERROR",
                    (
                        f"Failed to fetch "
                        f"from {provider_name} "
                        f"for market "
                        f"{market_id}: "
                        f"{error}"
                    ),
                )

                run_log.errors.append(
                    (
                        f"Provider "
                        f"{provider_name}: "
                        f"{error}"
                    )
                )

        run_log.end_time = datetime.now(
            timezone.utc
        ).isoformat()

        self.audit_logger.log(
            "INGESTION_RUN_COMPLETED",
            (
                f"Market '{market_id}' "
                "finished. "
                f"Inserted: "
                f"{run_log.records_inserted}, "
                f"Skipped: "
                f"{run_log.records_skipped}"
            ),
        )

        return run_log
