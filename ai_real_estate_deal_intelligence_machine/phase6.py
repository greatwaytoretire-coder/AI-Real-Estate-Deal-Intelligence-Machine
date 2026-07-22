from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ARVEstimate:
    low: float
    high: float
    confidence: float
    source: str
    assumptions: Optional[List[str]] = None


@dataclass
class RepairItem:
    category: str
    low: float
    high: float
    confidence: float = 0.75


@dataclass
class RepairEstimate:
    low: float
    high: float
    confidence: float
    source: str
    assumptions: List[str]
    repairs: List[RepairItem]


class ComparableSalesAgent:
    """Phase 6 comparable sales foundation."""

    def identify_comparables(self) -> List[Dict[str, Any]]:
        return [
            {"comparable": "comp-001", "sale_price": 210000, "distance": 0.8, "confidence": 0.88},
            {"comparable": "comp-002", "sale_price": 205000, "distance": 1.2, "confidence": 0.83},
            {"comparable": "comp-003", "sale_price": 198000, "distance": 1.7, "confidence": 0.76},
        ]


class ARVAgent:
    """Phase 6 ARV estimation foundation."""

    def estimate_arv(self) -> ARVEstimate:
        return ARVEstimate(
            low=180000,
            high=195000,
            confidence=0.85,
            source="mock-comparables",
            assumptions=["comparable weighted average", "condition adjusted"],
        )


class RepairEstimationAgent:
    """Phase 6 repair estimate foundation."""

    def estimate_repairs(self) -> RepairEstimate:
        return RepairEstimate(
            low=10000,
            high=15000,
            confidence=0.78,
            source="mock-condition-signals",
            assumptions=["roof", "hvac", "plumbing", "bathrooms", "kitchen", "windows"],
            repairs=[
                RepairItem(category="roof", low=3000, high=5000),
                RepairItem(category="hvac", low=2000, high=3500),
                RepairItem(category="plumbing", low=1500, high=3000),
            ],
        )
