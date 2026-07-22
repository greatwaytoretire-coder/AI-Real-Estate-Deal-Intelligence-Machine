from __future__ import annotations

import csv
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional


class ProviderStatus(str, Enum):
    ONLINE = "ONLINE"
    OFFLINE = "OFFLINE"
    DEGRADED = "DEGRADED"
    RATE_LIMITED = "RATE_LIMITED"
    ERROR = "ERROR"


@dataclass
class ProviderSyncSchedule:
    interval_minutes: int = 15
    enabled: bool = True


@dataclass
class IngestionEvent:
    event_type: str
    payload: Dict[str, Any]
    source: str = "local"


class ProviderRegistry:
    """Phase 2 provider registry using local mock and CSV-backed providers."""

    def __init__(self) -> None:
        self.providers = [
            CSVImportProvider("tests/sample_property_data.csv"),
            MockPropertyProvider(),
            MockBuyerProvider(),
            MockMarketProvider(),
            MockTransactionProvider(),
            MockGovernmentProvider(),
        ]


@dataclass
class ProviderHealth:
    status: ProviderStatus = ProviderStatus.ONLINE
    rate_limit_remaining: int = 100
    error_count: int = 0
    last_sync_at: Optional[str] = None
    freshness_minutes: int = 0


class CSVImportProvider:
    def __init__(self, file_path: str) -> None:
        self.file_path = Path(file_path)

    def fetch_records(self) -> List[IngestionEvent]:
        events: List[IngestionEvent] = []
        with self.file_path.open("r", encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                events.append(
                    IngestionEvent(
                        event_type="NEW_RECORD_RECEIVED",
                        payload={
                            "address": row.get("address"),
                            "market": row.get("market"),
                            "price": row.get("price"),
                            "source_type": row.get("source_type"),
                        },
                        source="csv-import",
                    )
                )
        return events


class MockPropertyProvider:
    def fetch_records(self) -> List[IngestionEvent]:
        return [
            IngestionEvent(
                event_type="NEW_PROPERTY_DISCOVERED",
                payload={"market": "Phoenix", "address": "101 Mock Street", "price": 215000},
                source="mock-property",
            )
        ]


class MockBuyerProvider:
    def fetch_records(self) -> List[IngestionEvent]:
        return [
            IngestionEvent(
                event_type="NEW_BUYER_SIGNAL",
                payload={"buyer": "Mock Buyer Alpha", "demand_score": 88},
                source="mock-buyer",
            )
        ]


class MockMarketProvider:
    def fetch_records(self) -> List[IngestionEvent]:
        return [
            IngestionEvent(
                event_type="MARKET_SCORE_CHANGED",
                payload={"market": "Phoenix", "score": 87},
                source="mock-market",
            )
        ]


class MockTransactionProvider:
    def fetch_records(self) -> List[IngestionEvent]:
        return [
            IngestionEvent(
                event_type="OFFER_RECEIVED",
                payload={"deal_id": "deal-1", "offer_price": 200000},
                source="mock-transaction",
            )
        ]


class MockGovernmentProvider:
    def fetch_records(self) -> List[IngestionEvent]:
        return [
            IngestionEvent(
                event_type="GOVERNMENT_RECORD_RECEIVED",
                payload={"jurisdiction": "Phoenix", "record_type": "permit"},
                source="mock-government",
            )
        ]


class IngestionEngine:
    def __init__(self) -> None:
        self.registry = ProviderRegistry()
        self.schedule = ProviderSyncSchedule()

    def ingest_sample_data(self) -> List[Dict[str, Any]]:
        normalized_records: List[Dict[str, Any]] = []
        for provider in self.registry.providers:
            for event in provider.fetch_records():
                normalized = {
                    "event_type": event.event_type,
                    "source": event.source,
                    "record": event.payload,
                    "normalized": True,
                    "deduplicated": True,
                    "confidence_score": 0.85,
                }
                normalized_records.append(normalized)
        return normalized_records
