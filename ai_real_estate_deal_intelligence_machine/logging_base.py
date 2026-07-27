from __future__ import annotations

from typing import Protocol


class LoggingProtocol(Protocol):
    """Defines a standard interface for logging system events."""

    def log(self, event_type: str, message: str) -> None:
        """Logs a message with a specific event type."""
        ...
