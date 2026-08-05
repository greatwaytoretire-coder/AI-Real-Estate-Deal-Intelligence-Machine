from __future__ import annotations

from typing import Dict, List

from ai_real_estate_deal_intelligence_machine.transaction.transaction_models import (
    TransactionState,
)


class TransactionCoordinator:
    """
    Coordinates the real estate transaction lifecycle.

    Future integrations:
    - Workflow automation
    - Agent orchestration
    - CRM updates
    - Closing systems
    """

    WORKFLOW_STAGES = [
        "ACQUISITION",
        "UNDERWRITING",
        "NEGOTIATION",
        "BUYER_MATCHING",
        "PACKAGING",
        "DISPOSITION",
    ]

    def start_transaction(
        self,
        property_data: Dict,
    ) -> TransactionState:

        return TransactionState(
            property_id=property_data.get(
                "property_id",
                "PROP-001",
            ),
            address=property_data.get(
                "address",
                "Unknown Address",
            ),
            current_stage="ACQUISITION",
            completed_stages=[],
            status="ACTIVE",
            notes=[
                "Transaction workflow started."
            ],
        )

    def complete_stage(
        self,
        transaction: TransactionState,
        stage: str,
    ) -> TransactionState:

        if stage not in transaction.completed_stages:
            transaction.completed_stages.append(stage)

        transaction.current_stage = stage

        transaction.notes.append(
            f"{stage} completed."
        )

        if len(transaction.completed_stages) == len(
            self.WORKFLOW_STAGES
        ):
            transaction.status = "COMPLETED"

        return transaction