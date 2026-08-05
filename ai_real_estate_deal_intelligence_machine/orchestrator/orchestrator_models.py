from dataclasses import dataclass
from typing import List


@dataclass
class WorkflowResult:
    deal_id: str
    completed_steps: List[str]
    status: str
    summary: str