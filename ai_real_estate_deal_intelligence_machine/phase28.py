from __future__ import annotations

import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Set

from .audit_logger import AuditLogger


class AutonomyLevel(int, Enum):
    """Defines the operational autonomy level of the system."""

    MANUAL = 0
    RECOMMENDATIONS_ONLY = 1
    HUMAN_IN_THE_LOOP = 2
    LIMITED_AUTONOMY = 3
    CONTROLLED_AUTONOMY = 4


@dataclass
class SystemState:
    """Manages the global state, including emergency stop and autonomy level."""

    audit_logger: AuditLogger
    emergency_stop_activated: bool = False
    current_autonomy_level: AutonomyLevel = AutonomyLevel.HUMAN_IN_THE_LOOP

    def activate_emergency_stop(self, operator_id: str, reason: str):
        """Activates the global emergency stop, halting all external actions."""
        if not self.emergency_stop_activated:
            self.emergency_stop_activated = True
            self.audit_logger.log("EMERGENCY_STOP", f"ACTIVATED by {operator_id}. Reason: {reason}")

    def deactivate_emergency_stop(self, operator_id: str, reason: str):
        """Deactivates the global emergency stop."""
        if self.emergency_stop_activated:
            self.emergency_stop_activated = False
            self.audit_logger.log("EMERGENCY_STOP", f"DEACTIVATED by {operator_id}. Reason: {reason}")

    def set_autonomy_level(self, level: AutonomyLevel, operator_id: str):
        """Sets the system's autonomy level."""
        if self.current_autonomy_level != level:
            self.current_autonomy_level = level
            self.audit_logger.log("AUTONOMY_CHANGE", f"Level set to {level.name} by {operator_id}.")


@dataclass
class Job:
    """Represents a job to be processed, with retry tracking."""

    job_id: str
    payload: Dict[str, Any]
    attempts: int = 0


class ReliabilityEngine:
    """Simulates a reliable job processing system with retries and a DLQ."""

    def __init__(self, system_state: SystemState, max_retries: int = 3):
        self.system_state = system_state
        self.max_retries = max_retries
        self.job_queue: List[Job] = []
        self.dead_letter_queue: List[Job] = []
        self.processed_ids: Set[str] = set()

    def submit_job(self, job_id: str, payload: Dict[str, Any]) -> bool:
        """Submits a job, preventing duplicates (idempotency)."""
        if job_id in self.processed_ids:
            self.system_state.audit_logger.log("RELIABILITY", f"Duplicate job {job_id} ignored.")
            return False
        self.job_queue.append(Job(job_id=job_id, payload=payload))
        return True

    def process_queue(self, failure_simulation: Dict[str, Any] = None):
        """Processes jobs from the queue with retry and DLQ logic."""
        if self.system_state.emergency_stop_activated:
            return

        job_to_process = self.job_queue.pop(0)
        job_to_process.attempts += 1

        try:
            # Simulate processing and potential failure
            if failure_simulation and failure_simulation.get("job_id") == job_to_process.job_id:
                if job_to_process.attempts <= failure_simulation.get("fail_attempts", 0):
                    raise ConnectionError("Simulated provider failure")

            # On success
            self.processed_ids.add(job_to_process.job_id)
            self.system_state.audit_logger.log("RELIABILITY", f"Job {job_to_process.job_id} processed successfully.")
        except Exception as e:
            self.system_state.audit_logger.log("RELIABILITY_ERROR", f"Job {job_to_process.job_id} failed on attempt {job_to_process.attempts}: {e}")
            if job_to_process.attempts >= self.max_retries:
                self.dead_letter_queue.append(job_to_process)
                self.system_state.audit_logger.log("RELIABILITY_DLQ", f"Job {job_to_process.job_id} moved to DLQ.")
            else:
                # Re-queue with exponential backoff (simulation)
                backoff_time = 2 ** job_to_process.attempts
                self.system_state.audit_logger.log("RELIABILITY", f"Re-queuing job {job_to_process.job_id}. Backoff: {backoff_time}s")
                self.job_queue.append(job_to_process)


class SafetyControls:
    """Centralized safety checks before performing sensitive actions."""

    def __init__(self, system_state: SystemState):
        self.system_state = system_state
        # Mock databases for consent and opt-outs
        self.consent_db = {"user-123"}
        self.opt_out_db = {"user-456"}

    def check(self, action_type: str, user_id: str, required_autonomy: AutonomyLevel) -> bool:
        """Runs all safety checks. Returns True if safe, False otherwise."""
        # 1. Emergency Stop
        if self.system_state.emergency_stop_activated:
            self.system_state.audit_logger.log("SAFETY_CHECK_FAIL", "Emergency stop is active.")
            return False

        # 2. Autonomy Level
        if self.system_state.current_autonomy_level < required_autonomy:
            self.system_state.audit_logger.log("SAFETY_CHECK_FAIL", f"Autonomy level {self.system_state.current_autonomy_level.name} is below required {required_autonomy.name}.")
            return False

        # 3. Consent and Opt-Out
        if user_id not in self.consent_db or user_id in self.opt_out_db:
            self.system_state.audit_logger.log("SAFETY_CHECK_FAIL", f"Consent/opt-out check failed for user {user_id}.")
            return False

        # 4. Rate Limiting (Simulated)
        # In a real system, this would check against Redis or a similar store.

        self.system_state.audit_logger.log("SAFETY_CHECK_PASS", f"Action '{action_type}' for user '{user_id}' passed all safety checks.")
        return True