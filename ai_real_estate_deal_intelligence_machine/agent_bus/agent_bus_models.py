from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class AgentRequest:
    agent_name: str
    action: str
    payload: Dict[str, Any]


@dataclass
class AgentResponse:
    agent_name: str
    success: bool
    result: Any
    message: str