from dataclasses import dataclass
from typing import List


@dataclass
class WorkflowExecutionResult:
    deal_id: str
    completed_agents: List[str]
    status: str
    message: str