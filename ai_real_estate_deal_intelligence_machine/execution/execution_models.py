from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class ExecutionTask:

    task_name: str

    status: str = "PENDING"

    result: str = ""


@dataclass
class DealExecutionPlan:

    property_id: str

    tasks: List[ExecutionTask] = field(
        default_factory=list
    )

    status: str = "CREATED"