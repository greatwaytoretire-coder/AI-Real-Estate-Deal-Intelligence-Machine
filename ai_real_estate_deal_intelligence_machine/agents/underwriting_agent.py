from ai_real_estate_deal_intelligence_machine.intelligence.deal_intelligence_coordinator import (
    DealIntelligenceCoordinator,
)


class UnderwritingAgent:
    """
    Autonomous underwriting intelligence agent.

    Converts a property opportunity into
    an investor intelligence package.
    """


    def __init__(self):

        self.coordinator = DealIntelligenceCoordinator()



    def process(
        self,
        payload: dict,
    ):

        result = self.coordinator.analyze(

            property_id=payload.get(
                "property_id",
                "PROPERTY-001"
            ),

            purchase_price=payload.get(
                "purchase_price",
                150000
            ),

            estimated_value=payload.get(
                "estimated_value",
                275000
            ),

            repair_cost=payload.get(
                "repair_cost",
                30000
            ),
        )


        return {

            "property_id":
                result.property_id,

            "deal_score":
                result.deal_score,

            "recommendation":
                result.recommendation,

            "priority":
                result.priority,

            "projected_profit":
                result.projected_profit,

            "mao":
                result.mao,

            "profit_margin":
                result.profit_margin,

            "risk_level":
                result.risk_level,

            "status":
                result.status,
        }