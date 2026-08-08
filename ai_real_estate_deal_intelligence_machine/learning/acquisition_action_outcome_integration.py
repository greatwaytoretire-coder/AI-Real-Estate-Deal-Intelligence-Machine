from __future__ import annotations

from typing import Any, Dict, List

from .acquisition_action_outcome_verifier import (
    AcquisitionActionOutcomeVerifier,
)


class AcquisitionActionOutcomeIntegration:
    """
    Integration layer connecting authorized action execution
    results to outcome verification and state reconciliation.
    """

    def __init__(self) -> None:
        self.verifier = AcquisitionActionOutcomeVerifier()

    def analyze(
        self,
        execution_result: Dict[str, Any],
    ) -> Dict[str, Any]:
        executions: List[Dict[str, Any]] = execution_result.get(
            "executions",
            []
        )

        verification = self.verifier.verify_executions(executions)

        return {
            "source_status": execution_result.get("status"),
            "verification": verification,
            "status": (
                "ACQUISITION_ACTION_OUTCOME_INTEGRATION_COMPLETE"
            ),
        }