from __future__ import annotations

import time
from threading import Event

from .logging_base import LoggingProtocol
from .phase30 import ContinuousRuntime
from .phase37 import MultiMarketOrchestrator


class SystemSupervisor:
    """
    A top-level process supervisor that orchestrates the continuous operation
    of the AI Deal Machine. It coordinates market ingestion and job processing.
    """

    def __init__(
        self,
        multi_market_orchestrator: MultiMarketOrchestrator,
        runtime: ContinuousRuntime,
        audit_logger: LoggingProtocol,
        poll_interval: int = 60,
    ):
        self.multi_market_orchestrator = multi_market_orchestrator
        self.runtime = runtime
        self.audit_logger = audit_logger
        self.poll_interval = poll_interval
        self._stop_event = Event()

    def run_single_cycle(self):
        """Runs one full cycle of ingestion and job processing."""
        self.audit_logger.log("SUPERVISOR_CYCLE_START", "Starting new supervisor cycle.")

        # 1. Trigger ingestion for all active markets to discover opportunities
        self.multi_market_orchestrator.run_all_active_markets({})
        self.audit_logger.log("SUPERVISOR_INGESTION_COMPLETE", "Market ingestion phase complete.")

        # 2. Process all pending jobs until the queue is empty
        while self.runtime.job_queue.pending_queue and not self._stop_event.is_set():
            self.runtime.worker.run()

        self.audit_logger.log("SUPERVISOR_CYCLE_COMPLETE", "Job processing phase complete.")

    def run_continuously(self):
        """Runs the main continuous processing loop of the application."""
        self.audit_logger.log("SUPERVISOR_START", "System Supervisor starting continuous operation.")
        while not self._stop_event.is_set():
            try:
                self.run_single_cycle()
                self.audit_logger.log("SUPERVISOR_SLEEP", f"Cycle finished. Sleeping for {self.poll_interval} seconds.")
                self._stop_event.wait(self.poll_interval)
            except (Exception, KeyboardInterrupt) as e:
                self.audit_logger.log("SUPERVISOR_ERROR", f"An unhandled error occurred in the main loop: {e}")
                self._stop_event.wait(self.poll_interval) # Wait before retrying

    def stop(self):
        """Signals the continuous loop to stop gracefully."""
        self.audit_logger.log("SUPERVISOR_STOP", "Stop signal received. Shutting down after current cycle.")
        self._stop_event.set()