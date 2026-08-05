from datetime import datetime, timezone

from .observability_models import (
    EventType,
    SystemEvent,
    ObservabilityReport,
)


class EventLogger:
    """
    Production observability event tracking foundation.

    Records system, AI agent, and workflow events.
    """

    def __init__(self):
        self.events = []

    def record_event(
        self,
        source: str,
        message: str,
        event_type: EventType = EventType.INFO,
    ):
        event = SystemEvent(
            event_type=event_type,
            source=source,
            message=message,
            created_at=datetime.now(timezone.utc),
        )

        self.events.append(event)

        return event

    def generate_report(self):

        errors = sum(
            1
            for event in self.events
            if event.event_type == EventType.ERROR
        )

        warnings = sum(
            1
            for event in self.events
            if event.event_type == EventType.WARNING
        )

        return ObservabilityReport(
            total_events=len(self.events),
            error_events=errors,
            warning_events=warnings,
            generated_at=datetime.now(timezone.utc),
        )