from __future__ import annotations

from typing import Any, Dict

from .acquisition_action_outcome_resolution import (
    AcquisitionActionOutcomeResolver,
)


class AcquisitionActionOutcomeResolutionIntegration:
    """
    Integration boundary between Part 29 outcome verification and
    Part 30 outcome resolution.
    """

    STATUS = "ACQUISITION_ACTION_OUTCOME_RESOLUTION_INTEGRATION_COMPLETE"

    def __init__(self) -> None:
        self.resolver = AcquisitionActionOutcomeResolver()

    def run(
        self,
        verification: Dict[str, Any],
    ) -> Dict[str, Any]:
        resolution = self.resolver.resolve(verification)

        return {
            "source_status": resolution.get("status"),
            "status": self.STATUS,
            "resolution": resolution,
        }


def run_acquisition_action_outcome_resolution(
    verification: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Convenience entry point for Part 30 integration.
    """

    integration = AcquisitionActionOutcomeResolutionIntegration()

    return integration.run(verification)