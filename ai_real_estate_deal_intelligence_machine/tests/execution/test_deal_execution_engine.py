from ai_real_estate_deal_intelligence_machine.execution.deal_execution_engine import (
    DealExecutionEngine,
)


def test_execution_plan_creation():

    engine = DealExecutionEngine()

    plan = engine.create_execution_plan(
        {
            "property_id": "PROP-001"
        }
    )

    assert plan.status == "READY"
    assert len(plan.tasks) == 5


def test_execute_task():

    engine = DealExecutionEngine()

    plan = engine.create_execution_plan(
        {
            "property_id": "PROP-001"
        }
    )

    engine.execute_task(
        plan,
        "RUN_UNDERWRITING",
    )

    task = plan.tasks[1]

    assert task.status == "COMPLETED"