from datetime import datetime, timezone

from .resilience_models import (
    RecoveryEvent,
    RecoveryStatus,
    ResilienceReport,
)


class ResilienceEngine:
    """
    Phase 103

    Foundation for production resiliency.
    """

    def __init__(self):
        self.events = []

    def record_event(
        self,
        component: str,
        status: RecoveryStatus,
        attempts: int = 1,
    ):

        event = RecoveryEvent(
            component=component,
            status=status,
            attempts=attempts,
            timestamp=datetime.now(timezone.utc),
        )

        self.events.append(event)

        return event

    def generate_report(self):

        recovered = sum(
            1
            for event in self.events
            if event.status == RecoveryStatus.RECOVERED
        )

        failed = sum(
            1
            for event in self.events
            if event.status == RecoveryStatus.FAILED
        )

        return ResilienceReport(
            total_events=len(self.events),
            recovered_events=recovered,
            failed_events=failed,
            generated_at=datetime.now(timezone.utc),
        )