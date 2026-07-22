from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class MarketScore:
    opportunity_density: float = 8.2
    buyer_density: float = 7.6
    investor_activity: float = 7.0
    property_turnover: float = 6.5
    price_movement: float = 6.8
    distress_signals: float = 5.4
    buyer_demand: float = 7.9
    market_liquidity: float = 7.5

    @property
    def value(self) -> float:
        return round(
            (
                self.opportunity_density
                + self.buyer_density
                + self.investor_activity
                + self.property_turnover
                + self.price_movement
                + self.distress_signals
                + self.buyer_demand
                + self.market_liquidity
            )
            / 8,
            2,
        )


@dataclass
class MarketSnapshot:
    market: str = "Phoenix"
    score: MarketScore = field(default_factory=MarketScore)

    def classify_market(self) -> List[str]:
        categories: List[str] = []
        if self.score.value >= 7.0:
            categories.append("TOP_MARKETS")
        if self.score.value >= 6.5:
            categories.append("EMERGING_MARKETS")
        if self.score.opportunity_density >= 7.0:
            categories.append("HIGH-OPPORTUNITY_ZONES")
        if self.score.buyer_density >= 7.0:
            categories.append("HIGH-BUYER-DEMAND_ZONES")
        if self.score.distress_signals <= 5.0:
            categories.append("UNDER-SERVED_MARKETS")
        return categories


class MarketIntelligenceAgent:
    """Phase 3 market intelligence agent with explainable mock scoring."""

    def __init__(self) -> None:
        self._snapshots = {
            "Phoenix": MarketSnapshot(market="Phoenix"),
            "Tucson": MarketSnapshot(market="Tucson", score=MarketScore(opportunity_density=6.3, buyer_density=6.1, investor_activity=5.8, property_turnover=6.0, price_movement=6.1, distress_signals=5.6, buyer_demand=6.0, market_liquidity=5.9)),
            "Dallas": MarketSnapshot(market="Dallas", score=MarketScore(opportunity_density=7.8, buyer_density=8.1, investor_activity=7.5, property_turnover=7.0, price_movement=7.2, distress_signals=5.1, buyer_demand=7.8, market_liquidity=7.8)),
        }

    def rank_markets(self) -> List[Dict[str, Any]]:
        rankings: List[Dict[str, Any]] = []
        for market, snapshot in self._snapshots.items():
            rankings.append(
                {
                    "market": market,
                    "market_score": snapshot.score.value,
                    "opportunity_density": snapshot.score.opportunity_density,
                    "buyer_density": snapshot.score.buyer_density,
                    "market_liquidity": snapshot.score.market_liquidity,
                    "category": snapshot.classify_market(),
                }
            )
        rankings.sort(key=lambda row: row["market_score"], reverse=True)
        return rankings


class HeatMapEngine:
    """Produces the required Phase 3 heat map outputs in a local mock form."""

    def generate_maps(self) -> Dict[str, Dict[str, Any]]:
        return {
            "opportunity_heat_map": {"market": "Phoenix", "score": 8.2},
            "buyer_heat_map": {"market": "Phoenix", "score": 7.6},
            "distress_heat_map": {"market": "Dallas", "score": 5.1},
            "investor_activity_heat_map": {"market": "Dallas", "score": 7.5},
            "buyer_opportunity_overlap_map": {"market": "Phoenix", "score": 8.1},
        }


class MarketAlertSystem:
    def __init__(self) -> None:
        self.alerts: List[Dict[str, Any]] = []

    def create_alert(self, market: str, old_score: float, new_score: float) -> Dict[str, Any]:
        alert = {
            "market": market,
            "old_score": old_score,
            "new_score": new_score,
            "material_change": abs(new_score - old_score) >= 0.5,
        }
        self.alerts.append(alert)
        return alert
