import unittest
from pathlib import Path

from .main import create_production_services
from .phase30 import ContinuousRuntime # type: ignore
from .phase36 import AgentOrchestrator
from .phase5 import OpportunityScoringEngine, ScoringOutput
from .phase8 import DealRiskAgent, DealRiskAgentInput
from .jobs.base import Job
from .persistent_job_queue import PersistentJobQueue
from .persistent_deduplication_engine import PersistentDeduplicationEngine


class MainBootstrapTest(unittest.TestCase):
    def test_production_bootstrap_creates_valid_runtime(self):
        """
        Verify the production bootstrap correctly creates and wires all services.
        """
        services = create_production_services()
        runtime = services["runtime"]

        # 1. Verify the top-level object is correct
        self.assertIsInstance(runtime, ContinuousRuntime)
        self.assertIsNotNone(runtime.orchestrator)
        self.assertIsNotNone(runtime.provider_manager)
        self.assertIsNotNone(runtime.scaling_manager)

        # 2. Verify the orchestrator and workflow are configured
        orchestrator = services["orchestrator"]
        self.assertIsInstance(orchestrator, AgentOrchestrator)
        self.assertIn("PROPERTY_DISCOVERED", orchestrator.workflow_registry)

        workflow = orchestrator.workflow_registry["PROPERTY_DISCOVERED"]
        self.assertEqual(len(workflow.steps), 2)
        self.assertIsInstance(workflow.steps[0], DealRiskAgent)
        self.assertTrue(callable(workflow.input_factories["DealRiskAgent"]))
        self.assertIsInstance(workflow.steps[1], OpportunityScoringEngine)
        self.assertTrue(callable(workflow.input_factories["OpportunityScoringEngine"]))

    def test_production_workflow_executes_correctly(self):
        """
        Verify a job can be processed using the production-configured workflow
        without relying on any test-defined factories.
        """
        services = create_production_services()
        runtime = services["runtime"]

        # Create a representative job
        job = Job(
            job_id="job-prod-test-01",
            payload={"event_type": "PROPERTY_DISCOVERED", "entity_id": "deal-xyz", "market_id": "test_market"},
        )

        # Execute the job through the orchestrator
        # This will use the factories and agents configured in main.py
        output = runtime.orchestrator.handle_job(job)

        # Verify the workflow completed without error
        self.assertIsNone(output.error)
        self.assertIsInstance(output, ScoringOutput) # The last agent's output

    def test_production_runtime_uses_persistent_components(self):
        """
        STEP 5: Verify the production composition root injects the correct
        persistent queue and deduplication engine into the runtime.
        """
        services = create_production_services()
        runtime = services["runtime"]

        # Verify that the runtime is configured with the persistent implementations
        self.assertIsInstance(runtime.job_queue, PersistentJobQueue)
        self.assertIsInstance(runtime.deduplication_engine, PersistentDeduplicationEngine)

        # Verify they are connected to the same database client instance
        db_client_from_main = services["db_client"]
        self.assertIs(runtime.job_queue.db_client, db_client_from_main)
        self.assertIs(runtime.deduplication_engine.db_client, db_client_from_main)

    def test_production_service_dictionary_integrity(self):
        """
        STEP 5: Verify the service dictionary contains the expected components
        and that they are wired correctly.
        """
        services = create_production_services()

        # Verify all expected top-level services are present
        self.assertIn("runtime", services)
        self.assertIn("multi_market_orchestrator", services)
        self.assertIn("audit_logger", services)
        self.assertIn("db_client", services)

        # Verify that the MultiMarketOrchestrator uses the same runtime instance
        self.assertIs(services["multi_market_orchestrator"].runtime, services["runtime"])
