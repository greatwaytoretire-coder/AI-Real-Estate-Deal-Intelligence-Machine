from __future__ import annotations

from typing import Any

from .intelligence_models import IntelligencePacket


class DataPipeline:
    """
    Collects provider outputs into a single packet.
    """

    def build_packet(
        self,
        property_data: dict[str, Any],
        county_data: dict[str, Any],
        market_data: dict[str, Any],
        valuation_data: dict[str, Any],
    ) -> IntelligencePacket:

        return IntelligencePacket(
            property_data=property_data,
            county_data=county_data,
            market_data=market_data,
            valuation_data=valuation_data,
            confidence_score=0.90,
            overall_score=85.0,
        )