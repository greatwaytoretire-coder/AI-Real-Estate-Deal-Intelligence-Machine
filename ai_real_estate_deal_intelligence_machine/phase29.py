from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List


class MarketStatus(str, Enum):
    """Defines the monitoring status of a market."""
    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"
    FAILED = "FAILED"
    NEEDS_REVIEW = "NEEDS_REVIEW"

@dataclass
class MarketUsage:
    """Tracks usage against configured limits for a market."""

    api_calls: int = 0
    deals_analyzed: int = 0
    cost_incurred: float = 0.0


@dataclass
class MarketConfig:
    """Configuration for a single market in a multi-market environment."""

    market_id: str
    market_name: str
    status: MarketStatus = MarketStatus.ACTIVE

    # Market-specific settings
    data_providers: List[str] = field(default_factory=list)
    underwriting_assumptions: Dict[str, Any] = field(default_factory=dict)
    scoring_model_version: str = "default_v1"

    # Budget and usage limits
    monthly_budget: float = 1000.0  # Default budget
    api_call_limit: int = 10000


class ScalingManager:
    """Manages configurations and state for multiple markets."""

    def __init__(self):
        self.market_configs: Dict[str, MarketConfig] = {}
        self.market_usage: Dict[str, MarketUsage] = {}

    def load_market_config(self, config: MarketConfig):
        """Loads or updates the configuration for a market."""
        self.market_configs[config.market_id] = config
        if config.market_id not in self.market_usage:
            self.market_usage[config.market_id] = MarketUsage()

    def get_market_config(self, market_id: str) -> MarketConfig | None:
        """Retrieves the configuration for a specific market."""
        return self.market_configs.get(market_id)

    def get_active_markets(self) -> List[MarketConfig]:
        """Returns a list of all enabled market configurations."""
        return [config for config in self.market_configs.values() if config.status == MarketStatus.ACTIVE]

    def is_within_budget(self, market_id: str) -> bool:
        """Checks if a market is within its budget and usage limits."""
        config = self.get_market_config(market_id)
        usage = self.market_usage.get(market_id)

        if not config or not usage:
            return False

        if usage.cost_incurred >= config.monthly_budget:
            return False
        if usage.api_calls >= config.api_call_limit:
            return False

        return True

    def record_usage(self, market_id: str, api_calls: int, cost: float):
        """Records usage for a market."""
        if market_id in self.market_usage:
            self.market_usage[market_id].api_calls += api_calls
            self.market_usage[market_id].cost_incurred += cost