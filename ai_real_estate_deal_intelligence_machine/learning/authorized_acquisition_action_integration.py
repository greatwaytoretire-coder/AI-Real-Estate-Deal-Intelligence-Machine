from __future__ import annotations

from typing import Any, Dict, List

from .authorized_acquisition_action_executor import (
    AuthorizedAcquisitionActionExecutor,
)


class AuthorizedAcquisitionActionIntegration:
    """
    Sprint 4 Part 28 integration layer.

    Connects Sprint 4 Part 27 action-execution decisions to the
    authorized state-transition executor.
    """

    def __init__(self) -> None:
        self.executor = AuthorizedAcquisitionActionExecutor()

    def run(
        self,
        action_execution_results: Dict[str, Any],
    ) -> Dict[str, Any]:
        executions = action_execution_results.get("executions", [])

        results: List[Dict[str, Any]] = self.executor.execute(executions)

        return {
            **results,
            "source_status": action_execution_results.get("status"),
            "status": "AUTHORIZED_ACQUISITION_ACTION_INTEGRATION_COMPLETE",
        }