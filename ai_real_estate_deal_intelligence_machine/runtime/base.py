from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Protocol


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


class IngestionRunner(Protocol):
    """Defines the interface for running ingestion for a market."""

    def run_ingestion_for_market(
        self,
        market_id: str,
        query: Dict[str, Any],
    ) -> IngestionRun:
        """Runs a full ingestion cycle for a specific market."""
        ...