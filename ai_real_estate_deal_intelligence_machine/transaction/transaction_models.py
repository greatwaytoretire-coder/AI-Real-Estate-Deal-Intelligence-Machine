from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class TransactionState:

    property_id: str

    address: str

    current_stage: str

    completed_stages: List[str] = field(default_factory=list)

    status: str = "STARTED"

    notes: List[str] = field(default_factory=list)