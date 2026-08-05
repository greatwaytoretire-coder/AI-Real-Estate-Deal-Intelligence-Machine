from datetime import datetime, timezone

from .dashboard_models import (
    DealStatus,
    AgentStatus,
    AIRecommendation,
    DashboardSnapshot,
)


class DealDashboard:

    def __init__(self):
        self.deals = []
        self.agents = []
        self.recommendations = []

    def register_deal(
        self,
        deal_id: str,
        property_address: str,
        stage: str,
    ):
        self.deals.append(
            DealStatus(
                deal_id=deal_id,
                property_address=property_address,
                status="active",
                current_stage=stage,
                updated_at=datetime.now(timezone.utc),
            )
        )

    def register_agent(
        self,
        agent_name: str,
        task: str,
    ):
        self.agents.append(
            AgentStatus(
                agent_name=agent_name,
                status="running",
                current_task=task,
            )
        )

    def add_recommendation(
        self,
        deal_id: str,
        recommendation: str,
        confidence: float,
    ):
        self.recommendations.append(
            AIRecommendation(
                deal_id=deal_id,
                recommendation=recommendation,
                confidence_score=confidence,
            )
        )

    def snapshot(self):
        return DashboardSnapshot(
            deals=self.deals,
            agents=self.agents,
            recommendations=self.recommendations,
        )