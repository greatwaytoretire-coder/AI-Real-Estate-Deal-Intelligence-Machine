from __future__ import annotations

from threading import Event

from .logging_base import LoggingProtocol
from .phase30 import ContinuousRuntime
from .phase37 import MultiMarketOrchestrator


class SystemSupervisor:
    """
    Top-level supervisor for continuous AI Deal Machine operation.
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
        """
        Runs one ingestion + processing cycle.
        """

        if self._stop_event.is_set() and self.runtime.job_queue is None:
            return

        self.audit_logger.log(
            "SUPERVISOR_CYCLE_START",
            "Starting new supervisor cycle.",
        )

        try:
            self.multi_market_orchestrator.run_all_active_markets({})

            self.audit_logger.log(
                "SUPERVISOR_INGESTION_COMPLETE",
                "Market ingestion phase complete.",
            )

            while (
                self.runtime.job_queue.pending_queue
                and not self._stop_event.is_set()
            ):
                self.runtime.worker.run()

            self.audit_logger.log(
                "SUPERVISOR_CYCLE_COMPLETE",
                "Job processing phase complete.",
            )

        except Exception as e:
            self.audit_logger.log(
                "SUPERVISOR_ERROR",
                f"An unhandled error occurred in the main loop: {e}",
            )

    def run_continuously(self):
        """
        Runs the main continuous supervisor loop.
        """

        self.audit_logger.log(
            "SUPERVISOR_START",
            "System Supervisor starting continuous operation.",
        )

        while True:
            try:
                self.run_single_cycle()

                if self._stop_event.is_set():
                    break

                self.audit_logger.log(
                    "SUPERVISOR_SLEEP",
                    f"Cycle finished. Sleeping for {self.poll_interval} seconds.",
                )

                self._stop_event.wait(
                    self.poll_interval
                )

            except Exception as e:
                self.audit_logger.log(
                    "SUPERVISOR_ERROR",
                    f"An unhandled error occurred in the main loop: {e}",
                )
                break

    def stop(self):
        """
        Signals the supervisor to stop gracefully.
        """

        self.audit_logger.log(
            "SUPERVISOR_STOP",
            "Stop signal received. Shutting down after current cycle.",
        )

        self._stop_event.set()