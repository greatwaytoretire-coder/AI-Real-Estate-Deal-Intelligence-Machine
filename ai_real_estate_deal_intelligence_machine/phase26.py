from __future__ import annotations

import os
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Type

from .audit_logger import AuditLogger
from .phase24 import DataSourceType, PilotDataRecord
from .phase31 import AttomDataDownloader

@dataclass
class ProviderConfig:
    """Configuration for a data provider, including metadata for live integrations."""

    name: str
    label: str
    source_type: DataSourceType
    api_key_env_var: str | None = None
    cost_per_call: float = 0.0
    # Future fields: rate_limit_per_minute, retry_policy, etc.


class DataProvider(ABC):
    """Abstract base class for all data providers."""

    @abstractmethod
    def fetch(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Fetch data from the provider."""
        pass

    @abstractmethod
    def get_config(self) -> ProviderConfig:
        """Return the provider's configuration."""
        pass


class MockAttomProvider(DataProvider):
    """Mock provider for ATTOM data, used for fallback and testing."""

    def get_config(self) -> ProviderConfig:
        return ProviderConfig(name="attom_mock", label="ATTOM API (Mock)", source_type=DataSourceType.MOCK)

    def fetch(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        return [{"address": "123 Mock St", "attom_id": "12345", "source": "mock"}]


class ProviderManager:
    """Manages data providers, including fallback from live to mock."""

    def __init__(self, audit_logger: AuditLogger):
        self.audit_logger = audit_logger
        self.providers: Dict[str, DataProvider] = self._initialize_providers()

    def _initialize_providers(self) -> Dict[str, DataProvider]:
        """
        Initializes providers, respecting API key availability for live providers.
        Falls back to mocks if keys are not found.
        """
        initialized_providers: Dict[str, DataProvider] = {}

        # --- ATTOM Provider ---
        attom_api_key = os.getenv("ATTOM_API_KEY")
        if attom_api_key:
            provider = AttomDataDownloader(api_key=attom_api_key)
            initialized_providers["attom"] = provider
            self.audit_logger.log("PROVIDER_INIT", f"Initialized LIVE provider: {provider.get_config().label}")
        else:
            provider = MockAttomProvider()
            initialized_providers["attom"] = provider
            self.audit_logger.log("PROVIDER_INIT", f"ATTOM_API_KEY not found. Falling back to MOCK provider: {provider.get_config().label}")

        # --- Add other providers here following the same pattern ---

        return initialized_providers