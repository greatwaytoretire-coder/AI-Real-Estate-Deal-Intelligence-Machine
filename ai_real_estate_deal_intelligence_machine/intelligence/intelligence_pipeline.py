from __future__ import annotations

from .data_pipeline import DataPipeline
from .intelligence_models import IntelligencePacket


class IntelligencePipeline:
    """
    High-level pipeline used by the AI agents.
    """

    def __init__(self):

        self.pipeline = DataPipeline()

    def process(self) -> IntelligencePacket:

        property_data = {
            "address": "500 Intelligence Avenue",
            "price": 325000,
        }

        county_data = {
            "owner": "Demo Owner",
        }

        market_data = {
            "market_score": 91,
        }

        valuation_data = {
            "estimated_value": 338000,
        }

        return self.pipeline.build_packet(
            property_data,
            county_data,
            market_data,
            valuation_data,
        )