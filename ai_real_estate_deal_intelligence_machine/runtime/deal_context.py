from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class DealContext:
    """
    Shared object that moves through the
    autonomous pipeline.
    """

    deal_id: str

    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    opportunity: dict[str, Any] = field(default_factory=dict)

    seller = None

    financials = None

    intelligence = None

    buyers = None

    package = None

    execution = None

    recommendation: str = ""

    status: str = "STARTED"