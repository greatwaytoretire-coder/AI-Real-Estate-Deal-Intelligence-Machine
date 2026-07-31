from __future__ import annotations

from threading import Event

from .logging_base import LoggingProtocol
from .phase30 import ContinuousRuntime
from .phase37 import MultiMarketOrchestrator


class SystemSupervisor:
    """
    Top-level supervisor controlling continuous AI Deal Machine operation.
    """

    def __init__(
        self,
        multi_market_orchestrator: MultiMarketOrchestrator,
        runtime: ContinuousRuntime,
        audit_logger: LoggingProtocol,
        poll_interval: int = 60,
    ) -> None:

        self.multi_market_orchestrator = multi_market_orchestrator
        self.runtime = runtime
        self.audit_logger = audit_logger
        self.poll_interval = poll_interval
        self._stop_event = Event()


    def run_single_cycle(self) -> None:
        """
        Executes one complete supervisor cycle.
        """

        self.audit_logger.log(
            "SUPERVISOR_CYCLE_START",
            "Starting new supervisor cycle.",
        )

        try:
            report = (
                self.multi_market_orchestrator
                .run_all_active_markets({})
            )

            self.audit_logger.log(
                "SUPERVISOR_INGESTION_COMPLETE",
                f"Markets processed: {report.markets_processed}",
            )

            pending_jobs = len(
                self.runtime.job_queue.pending_queue
            )

            self.audit_logger.log(
                "SUPERVISOR_QUEUE_STATUS",
                f"Pending jobs: {pending_jobs}",
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


        except Exception as exc:

            self.audit_logger.log(
                "SUPERVISOR_ERROR",
                str(exc),
            )

            raise


    def run_continuously(self) -> None:
        """
        Runs the supervisor continuously until shutdown is requested.
        """

        self.audit_logger.log(
            "SUPERVISOR_START",
            "System Supervisor starting continuous operation.",
        )


        while not self._stop_event.is_set():

            try:
                self.run_single_cycle()


            except Exception as exc:

                self.audit_logger.log(
                    "SUPERVISOR_ERROR",
                    f"An unhandled error occurred in the main loop: {exc}",
                )


            if self._stop_event.is_set():
                break


            self.audit_logger.log(
                "SUPERVISOR_SLEEP",
                f"Sleeping {self.poll_interval} seconds.",
            )


            self._stop_event.wait(
                self.poll_interval
            )


    def stop(self) -> None:
        """
        Requests the supervisor to shut down.
        """

        self.audit_logger.log(
            "SUPERVISOR_STOP",
            "Shutdown requested.",
        )

        self._stop_event.set()