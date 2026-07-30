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
from .phase24 import DataSourceType


class OperatingMode(str, Enum):
    DEVELOPMENT = "development"
    MOCK = "mock"
    PILOT = "pilot"


@dataclass
class CanonicalProperty:
    canonical_id: str
    source_provider: str
    source_record_id: str
    address: str
    zip_code: str
    fingerprint: str


@dataclass
class RuntimeEvent:
    event_id: str = field(
        default_factory=lambda: f"evt_{uuid4()}"
    )
    event_type: str = "GENERIC_EVENT"
    entity_id: str = ""
    payload_ref: str = ""
    status: str = "PENDING"


class SystemState:

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

        event = RuntimeEvent(
            event_type=event_type,
            entity_id=entity_id,
            payload_ref=payload_ref,
        )

        self.runtime_events.append(event)

        return event


class ReliabilityEngine:

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

        self.processed_ids.add(job_id)
        self.system_state.processed_ids.add(job_id)


    def mark_failed(
        self,
        job_id: str,
    ) -> None:

        self.system_state.failed_ids.add(job_id)


class DeduplicationEngine:

    def __init__(self) -> None:

        self.processed_fingerprints: Dict[
            str,
            Set[str]
        ] = {}


    def is_duplicate(
        self,
        fingerprint: str,
        market_id: str,
    ) -> bool:

        return fingerprint in self.processed_fingerprints.get(
            market_id,
            set(),
        )


    def add(
        self,
        fingerprint: str,
        market_id: str,
    ) -> None:

        self.processed_fingerprints.setdefault(
            market_id,
            set(),
        ).add(fingerprint)


class NormalizationEngine:

    def normalize_property(
        self,
        raw_data: Dict[str, Any],
    ) -> CanonicalProperty:

        address = str(
            raw_data.get(
                "address",
                "",
            )
        ).strip()

        zip_code = str(
            raw_data.get(
                "zip",
                "",
            )
        ).strip()


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

    def __init__(self) -> None:

        self.jobs: Dict[str, Job] = {}
        self.pending_queue: List[str] = []
        self.dead_letter_queue: List[Job] = []


    def submit_job(
        self,
        job: Job,
    ) -> bool:

        if job.job_id in self.jobs:
            return False

        self.jobs[job.job_id] = job
        self.pending_queue.append(job.job_id)

        return True


    def get_pending_job(
        self,
    ) -> Optional[Job]:

        if not self.pending_queue:
            return None

        job_id = self.pending_queue.pop(0)

        job = self.jobs.get(job_id)

        if job:
            job.status = JobStatus.RUNNING

        return job


    def schedule_for_retry(
        self,
        job: Job,
    ) -> None:

        job.status = JobStatus.RETRY_SCHEDULED

        self.pending_queue.append(
            job.job_id
        )
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

        job = self.job_queue.get_pending_job()

        if job is None:
            return


        job.attempts += 1


        self.audit_logger.log(
            "WORKER_START",
            f"Worker started processing job {job.job_id}.",
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
                    f"Orchestration failed: {error_message}"
                )

            job.status = JobStatus.COMPLETED

            if self.db_client:

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
                "AI_PIPELINE_SUCCESS",
                f"AI pipeline completed successfully for job {job.job_id}.",
            )

            self.audit_logger.log(
                "WORKER_SUCCESS",
                f"Job {job.job_id} completed successfully.",
            )


        except Exception as error:

            self.audit_logger.log(
                "WORKER_ERROR",
                f"Job {job.job_id} failed: {error}",
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

            else:

                self.job_queue.schedule_for_retry(
                    job
                )


class ContinuousRuntime:

    def __init__(
        self,
        audit_logger: AuditLogger,
        provider_manager: ProviderManager,
        orchestrator: Any,
        scaling_manager: ScalingManager,
        job_queue: Optional[RuntimeJobQueue] = None,
        deduplication_engine: Optional[DeduplicationEngine] = None,
    ) -> None:


        self.mode = OperatingMode.DEVELOPMENT

        self.audit_logger = audit_logger
        self.provider_manager = provider_manager
        self.orchestrator = orchestrator
        self.scaling_manager = scaling_manager


        self.system_state = SystemState(
            audit_logger
        )


        self.reliability_engine = ReliabilityEngine(
            self.system_state
        )


        self.job_queue = (
            job_queue
            if job_queue
            else RuntimeJobQueue()
        )


        self.deduplication_engine = (
            deduplication_engine
            if deduplication_engine
            else DeduplicationEngine()
        )


        self.normalization_engine = NormalizationEngine()


        self.worker = Worker(
            job_queue=self.job_queue,
            audit_logger=self.audit_logger,
            reliability_engine=self.reliability_engine,
            orchestrator=self.orchestrator,
        )


        self.raw_data_store: List[
            Dict[str, Any]
        ] = []


        self.canonical_db: Dict[
            str,
            CanonicalProperty
        ] = {}

    def run_ingestion_for_market(
        self,
        market_id: str,
        query: Dict[str, Any],
    ) -> IngestionRun:
        """
        Executes ingestion for a configured market.

        Supports:
        - MOCK mode blocking
        - PILOT mode live providers
        - Deduplication
        - Normalization
        - Queue submission
        """

        market_config = self.scaling_manager.get_market_config(
            market_id
        )

        if not market_config:
            raise ValueError(
                f"Unknown market: {market_id}"
            )


        run_log = IngestionRun(
            provider="multi_provider",
            start_time=datetime.now(
                timezone.utc
            ).isoformat(),
        )

        for provider_name in market_config.data_providers:

            provider = self.provider_manager.providers.get(
                provider_name
            )
            print(type(provider))
            print(provider.get_config())

            if provider is None:

                self.audit_logger.log(
                    "PROVIDER_MISSING",
                    f"{provider_name} unavailable",
                )

                continue

            is_live = False

            config = None

            get_config = getattr(
                provider,
                "get_config",
                None,
            )

            if callable(get_config):
                try:
                    config = get_config()
                except Exception:
                    config = None

            if config is not None:
                source_type = getattr(
                    config,
                    "source_type",
                    None,
                )

                is_live = (
                    source_type == DataSourceType.LIVE
                )

            if (
                self.mode == OperatingMode.MOCK
                and is_live
            ):

                self.audit_logger.log(
                    "PROVIDER_BLOCKED",
                    f"{provider_name} blocked in MOCK mode",
                )

                continue

            try:

                records = provider.fetch(
                    query
                )

                run_log.records_discovered += len(
                    records
                )

                for record in records:

                    normalized = (
                        self.normalization_engine
                        .normalize_property(record)
                    )

                    if self.deduplication_engine.is_duplicate(
                        normalized.fingerprint,
                        market_id,
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

                    self.raw_data_store.append(
                        record
                    )

                    job = Job(
                        job_id=f"job_{uuid4()}",
                        payload={
                            "event_type": "PROPERTY_DISCOVERED",
                            "property_id": normalized.canonical_id,
                        },
                    )

                    self.job_queue.submit_job(
                        job
                    )

                    run_log.records_inserted += 1

            except Exception as exc:

                run_log.errors.append(
                    str(exc)
                )

                self.audit_logger.log(
                    "INGESTION_ERROR",
                    str(exc),
                )

        run_log.end_time = datetime.now(
            timezone.utc
        ).isoformat()

        self.audit_logger.log(
            "INGESTION_RUN_COMPLETED",
            (
                f"{market_id}: "
                f"{run_log.records_inserted} inserted"
            ),
        )

        return run_log