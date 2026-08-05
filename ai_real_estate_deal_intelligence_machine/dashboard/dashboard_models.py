from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class DealStatus:
    deal_id: str
    property_address: str
    status: str
    current_stage: str
    updated_at: datetime


@dataclass
class AgentStatus:
    agent_name: str
    status: str
    current_task: str


@dataclass
class AIRecommendation:
    deal_id: str
    recommendation: str
    confidence_score: float


@dataclass
class DashboardSnapshot:
    deals: List[DealStatus]
    agents: List[AgentStatus]
    recommendations: List[AIRecommendation]