from __future__ import annotations

import hashlib
import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Set
from uuid import uuid4

from .audit_logger import AuditLogger
from .phase28 import Job as ReliabilityJob
from .phase26 import ProviderManager
from .phase29 import ScalingManager
from .phase28 import ReliabilityEngine, SystemState


class OperatingMode(str, Enum):
    """Defines the operating mode of the system to enforce data separation."""

    DEVELOPMENT = "DEVELOPMENT"
    MOCK = "MOCK"
    PILOT = "PILOT"
    PRODUCTION = "PRODUCTION"


@dataclass
class IngestionRun:
    """Logs the metrics of a single data ingestion run."""

    provider: str
    start_time: str
    end_time: str | None = None
    records_discovered: int = 0
    records_inserted: int = 0
    records_updated: int = 0
    records_skipped: int = 0
    errors: List[str] = field(default_factory=list)


@dataclass
class CanonicalProperty:
    """A normalized, internal representation of a property."""

    canonical_id: str
    source_provider: str
    source_record_id: str
    address: str
    zip_code: str
    fingerprint: str  # A hash to detect duplicates


@dataclass
class RuntimeEvent:
    """A durable event representing a state change in the system."""

    event_id: str = field(default_factory=lambda: f"evt_{uuid4()}")
    event_type: str = "GENERIC_EVENT"
    entity_id: str = ""
    payload_ref: str = ""  # e.g., a path to the raw data in S3
    status: str = "PENDING"


class JobStatus(str, Enum):
    """Lifecycle of a job in the runtime queue."""

    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    RETRY_SCHEDULED = "RETRY_SCHEDULED"
    DEAD_LETTER = "DEAD_LETTER"


@dataclass
class Job(ReliabilityJob):
    """Extends the reliability job with a formal status."""

    status: JobStatus = JobStatus.PENDING


class DeduplicationEngine:
    """Prevents processing of duplicate records."""

    def __init__(self):
        # Use a dictionary to scope fingerprints by market_id
        self.processed_fingerprints: Dict[str, Set[str]] = {}

    def is_duplicate(self, fingerprint: str, market_id: str) -> bool:
        """Checks for a duplicate within a specific market."""
        return fingerprint in self.processed_fingerprints.get(market_id, set())

    def add(self, fingerprint: str, market_id: str):
        """Adds a fingerprint to a specific market's set."""
        self.processed_fingerprints.setdefault(market_id, set()).add(fingerprint)


class NormalizationEngine:
    """Converts raw provider data into a canonical internal format."""

    def normalize_property(self, raw_data: Dict[str, Any]) -> CanonicalProperty:
        address = str(raw_data.get("address", "")).strip().lower()
        zip_code = str(raw_data.get("zip", "")).strip()
        fingerprint = hashlib.sha256(f"{address}|{zip_code}".encode()).hexdigest()

        return CanonicalProperty(
            canonical_id=f"prop_{uuid4()}",
            source_provider=raw_data["provider"],
            source_record_id=raw_data["id"],
            address=address,
            zip_code=zip_code,
            fingerprint=fingerprint,
        )


class RuntimeJobQueue:
    """A more durable job queue simulation for the continuous runtime."""

    def __init__(self):
        self.jobs: Dict[str, Job] = {}
        self.pending_queue: List[str] = []
        self.dead_letter_queue: List[Job] = []

    def submit_job(self, job: Job) -> bool:
        if job.job_id in self.jobs:
            return False  # Idempotency
        self.jobs[job.job_id] = job
        self.pending_queue.append(job.job_id)
        return True

    def get_pending_job(self) -> Job | None:
        if not self.pending_queue:
            return None
        job_id = self.pending_queue.pop(0)
        job = self.jobs.get(job_id)
        if job:
            job.status = JobStatus.RUNNING
        return job


class Worker:
    """A worker that processes jobs from the queue."""

    def __init__(self, job_queue: RuntimeJobQueue, audit_logger: AuditLogger, reliability_engine: ReliabilityEngine, orchestrator):
        self.job_queue = job_queue
        self.audit_logger = audit_logger
        # This would be a real DB connection in production
        self.reliability_engine = reliability_engine
        self.orchestrator = orchestrator
        self.canonical_db: Dict[str, CanonicalProperty] = {}

    def run(self, failure_simulation: bool = False):
        """Picks up and executes one job."""
        job = self.job_queue.get_pending_job()
        if not job:
            return

        job.attempts += 1
        self.audit_logger.log("WORKER_START", f"Worker started processing job {job.job_id}.")
        try:
            if failure_simulation:
                raise ValueError("Simulated AI pipeline failure.")

            # Use the orchestrator to handle the job instead of the monolithic simulation
            output = self.orchestrator.handle_job(job)

            if output.error:
                raise RuntimeError(f"Orchestration failed: {output.error}")

            self.audit_logger.log("AI_PIPELINE_SUCCESS", f"Orchestrated job {job.job_id} finished successfully.")

            job.status = JobStatus.COMPLETED
            self.audit_logger.log("WORKER_SUCCESS", f"Job {job.job_id} completed successfully.")
            self.reliability_engine.processed_ids.add(job.job_id)
        except Exception as e:
            self.audit_logger.log("WORKER_ERROR", f"Job {job.job_id} failed: {e}")
            if job.attempts >= self.reliability_engine.max_retries:
                job.status = JobStatus.DEAD_LETTER
                self.job_queue.dead_letter_queue.append(job)
                self.audit_logger.log("RELIABILITY_DLQ", f"Job {job.job_id} moved to DLQ after {job.attempts} attempts.")
            else:
                job.status = JobStatus.RETRY_SCHEDULED
                self.job_queue.pending_queue.append(job.job_id) # Re-queue for retry
                self.audit_logger.log("RELIABILITY", f"Re-queuing job {job.job_id} for attempt {job.attempts + 1}.")


class ContinuousRuntime:
    """Orchestrates the continuous ingestion and processing of data."""

    def __init__(self, audit_logger: AuditLogger, provider_manager: ProviderManager, orchestrator, scaling_manager: ScalingManager):
        self.mode = OperatingMode.DEVELOPMENT
        self.audit_logger = audit_logger
        self.provider_manager = provider_manager
        self.orchestrator = orchestrator
        self.scaling_manager = scaling_manager
        # In a real system, SystemState would be shared (e.g., via Redis)
        self.system_state = SystemState(audit_logger=audit_logger)
        self.reliability_engine = ReliabilityEngine(system_state=self.system_state)
        self.deduplication_engine = DeduplicationEngine()
        self.normalization_engine = NormalizationEngine()
        self.job_queue = RuntimeJobQueue()
        self.worker = Worker(self.job_queue, self.audit_logger, self.reliability_engine, self.orchestrator)
        # In-memory stores for simulation
        self.raw_data_store: List[Dict[str, Any]] = []
        self.canonical_db: Dict[str, CanonicalProperty] = {}

    def run_ingestion_for_market(self, market_id: str, query: Dict[str, Any]) -> IngestionRun:
        """Runs a full ingestion cycle for a specific market."""
        market_config = self.scaling_manager.get_market_config(market_id)
        run_log = IngestionRun(provider=market_id, start_time=datetime.utcnow().isoformat())

        if not market_config or market_config.status != "ACTIVE":
            run_log.errors.append(f"Market '{market_id}' is not active or does not exist.")
            return run_log

        for provider_name in market_config.data_providers:
            provider = self.provider_manager.providers.get(provider_name)
            if not provider:
                run_log.errors.append(f"Provider '{provider_name}' for market '{market_id}' not found.")
                continue

            # Safety check: Do not use a live provider in MOCK mode.
            if self.mode == OperatingMode.MOCK and provider.get_config().source_type.value == "LIVE":
                self.audit_logger.log("INGESTION_SKIP", f"Skipping LIVE provider '{provider_name}' in MOCK mode.")
                continue

            try:
                raw_records = provider.fetch(query)
                for raw_record in raw_records:
                    run_log.records_discovered += 1
                    self.raw_data_store.append(raw_record)
                    normalized = self.normalization_engine.normalize_property(raw_record)

                    if self.deduplication_engine.is_duplicate(normalized.fingerprint, market_id):
                        run_log.records_skipped += 1
                        continue

                    self.deduplication_engine.add(normalized.fingerprint, market_id)
                    self.canonical_db[normalized.canonical_id] = normalized
                    run_log.records_inserted += 1

                    # Create a job to process this new canonical entity
                    job = Job(
                        job_id=f"process_{normalized.canonical_id}",
                        payload={"event_type": "PROPERTY_DISCOVERED", "entity_id": normalized.canonical_id, "market_id": market_id},
                    )
                    self.job_queue.submit_job(job)

            except Exception as e:
                self.audit_logger.log("INGESTION_ERROR", f"Failed to fetch from {provider_name} for market {market_id}: {e}")
                run_log.errors.append(f"Provider {provider_name}: {e}")

        run_log.end_time = datetime.utcnow().isoformat()
        self.audit_logger.log("INGESTION_RUN_COMPLETED", f"Market '{market_id}' finished. Inserted: {run_log.records_inserted}, Skipped: {run_log.records_skipped}")
        return run_log