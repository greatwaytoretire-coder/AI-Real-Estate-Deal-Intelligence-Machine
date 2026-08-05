from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class DealCommandRequest:
    deal_id: str
    property_address: str
    requested_action: str


@dataclass
class AgentAction:
    agent_name: str
    action: str
    result: str


@dataclass
class CommandCenterResult:
    deal_id: str
    status: str
    actions: List[AgentAction]
    completed_at: datetime