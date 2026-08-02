from dataclasses import dataclass

from ai_real_estate_deal_intelligence_machine.intelligence.deal_analyzer import (
    DealAnalyzer,
)

from ai_real_estate_deal_intelligence_machine.intelligence.recommendation_engine import (
    RecommendationEngine,
)


@dataclass
class AcquisitionPipelineResult:
    property_id: str
    qualified: bool
    deal_score: float
    recommendation: str
    pipeline_status: str

    @property
    def status(self) -> str:
        """
        Compatibility alias for workflow consumers.
        """

        return self.pipeline_status


class AcquisitionPipeline:

    def __init__(self):

        self.deal_analyzer = DealAnalyzer()

        self.recommendation_engine = RecommendationEngine()


    def qualify_property(
        self,
        purchase_price: float,
        estimated_value: float,
    ) -> bool:

        if estimated_value <= 0:
            return False

        if purchase_price <= 0:
            return False

        return purchase_price < estimated_value


    def execute(
        self,
        property_id: str,
        purchase_price: float,
        estimated_value: float,
        repair_cost: float,
    ) -> AcquisitionPipelineResult:


        qualified = self.qualify_property(
            purchase_price,
            estimated_value,
        )


        if not qualified:

            return AcquisitionPipelineResult(
                property_id=property_id,
                qualified=False,
                deal_score=0,
                recommendation="REJECT",
                pipeline_status="FAILED_QUALIFICATION",
            )


        analysis = self.deal_analyzer.analyze(
            property_id=property_id,
            purchase_price=purchase_price,
            estimated_value=estimated_value,
            repair_cost=repair_cost,
        )


        recommendation = (
            self.recommendation_engine.recommend(
                analysis
            )
        )


        return AcquisitionPipelineResult(
            property_id=property_id,
            qualified=True,
            deal_score=analysis.deal_score,
            recommendation=recommendation,
            pipeline_status="COMPLETED",
        )