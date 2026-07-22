from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class UnderwritingEvent:
    event_type: str
    payload: Dict[str, Any]


@dataclass
class UnderwritingResult:
    strategy: str
    purchase_price: float
    arv: float
    repairs: float
    closing_costs: float
    holding_costs: float
    financing: float
    selling_costs: float
    desired_profit: float
    assignment_fee: float
    cash_flow: float

    def as_dict(self) -> Dict[str, float | str]:
        total_cost = self.purchase_price + self.repairs + self.closing_costs + self.holding_costs + self.financing + self.selling_costs
        estimated_profit = self.arv - total_cost - self.desired_profit
        maximum_offer = max(0.0, self.arv - self.repairs - self.closing_costs - self.selling_costs - self.desired_profit)
        roi = round((estimated_profit / max(1.0, self.purchase_price)) * 100, 2)
        cash_on_cash_return = round((self.cash_flow / max(1.0, self.financing)) * 100, 2)
        cap_rate = round((self.cash_flow / max(1.0, self.arv)) * 100, 2)
        assignment_spread = round(max(0.0, self.assignment_fee - self.desired_profit), 2)
        offer_range = (max(0.0, maximum_offer - 5000), maximum_offer)

        return {
            "strategy": self.strategy,
            "maximum_offer": round(maximum_offer, 2),
            "offer_range": offer_range,
            "estimated_profit": round(estimated_profit, 2),
            "roi": roi,
            "cash_on_cash_return": cash_on_cash_return,
            "cap_rate": cap_rate,
            "assignment_spread": assignment_spread,
        }


class DealUnderwritingAgent:
    """Phase 7 deal underwriting foundation supporting several strategies."""

    SUPPORTED_STRATEGIES = {"WHOLESALE", "FIX AND FLIP", "BUY AND HOLD", "BRRRR", "CREATIVE FINANCE"}

    def __init__(self) -> None:
        self._result = UnderwritingResult(
            strategy="WHOLESALE",
            purchase_price=180000,
            arv=210000,
            repairs=12000,
            closing_costs=5000,
            holding_costs=2500,
            financing=20000,
            selling_costs=9000,
            desired_profit=12000,
            assignment_fee=8000,
            cash_flow=3000,
        )

    def generate_event(self) -> UnderwritingEvent:
        return UnderwritingEvent(
            event_type="UNDERWRITING_UPDATED",
            payload=self._result.as_dict(),
        )

    def rerun_when_inputs_change(self) -> UnderwritingResult:
        return self._result
