from ai_real_estate_deal_intelligence_machine.transaction.transaction_coordinator import (
    TransactionCoordinator,
)


def test_transaction_starts():

    coordinator = TransactionCoordinator()

    transaction = coordinator.start_transaction(
        {
            "property_id": "PROP-001",
            "address": "123 Main Street",
        }
    )

    assert transaction.status == "ACTIVE"
    assert transaction.current_stage == "ACQUISITION"


def test_transaction_stage_completion():

    coordinator = TransactionCoordinator()

    transaction = coordinator.start_transaction(
        {
            "property_id": "PROP-001",
            "address": "123 Main Street",
        }
    )

    coordinator.complete_stage(
        transaction,
        "UNDERWRITING",
    )

    assert "UNDERWRITING" in transaction.completed_stages