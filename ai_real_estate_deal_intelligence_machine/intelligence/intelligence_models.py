from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class IntelligencePacket:
    """
    Unified intelligence object passed throughout the AI system.
    """

    property_data: dict[str, Any] = field(default_factory=dict)
    county_data: dict[str, Any] = field(default_factory=dict)
    market_data: dict[str, Any] = field(default_factory=dict)
    valuation_data: dict[str, Any] = field(default_factory=dict)

    confidence_score: float = 0.0
    overall_score: float = 0.0

    metadata: dict[str, Any] = field(default_factory=dict)