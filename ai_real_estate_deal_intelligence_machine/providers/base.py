from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Dict, List

if TYPE_CHECKING:
    from ai_real_estate_deal_intelligence_machine.phase24 import DataSourceType


@dataclass
class ProviderConfig:
    """Configuration for a data provider, including metadata for live integrations."""

    name: str
    label: str
    source_type: "DataSourceType"
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
