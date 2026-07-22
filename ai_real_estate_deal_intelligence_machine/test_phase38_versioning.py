import unittest

from ai_real_estate_deal_intelligence_machine.phase38 import (
    ModelImprovementProposal,
    ModelRegistry,
    ModelVersionStatus,
)


class Phase38VersioningTest(unittest.TestCase):
    def setUp(self):
        self.registry = ModelRegistry()

    def test_model_versioning_lifecycle(self):
        """
        PHASE 38: Verify the full lifecycle of a model version.
        """
        # 1. Propose a new version
        proposal = ModelImprovementProposal(
            target_model="ARV_ESTIMATION",
            recommendation="New weights",
            supporting_deal_id="deal-001",
            error_analysis="Was off by 20%",
        )
        new_version = self.registry.propose_new_version(proposal)

        self.assertEqual(new_version.status, ModelVersionStatus.PROPOSED)
        self.assertEqual(new_version.model_name, "ARV_ESTIMATION")
        self.assertIsNone(self.registry.get_active_version("ARV_ESTIMATION"))

        # 2. Deploy the version (after simulated evaluation)
        new_version.status = ModelVersionStatus.EVALUATING
        deployed = self.registry.deploy_version(new_version.version_id)
        self.assertTrue(deployed)
        self.assertEqual(new_version.status, ModelVersionStatus.ACTIVE)
        self.assertIsNotNone(new_version.deployment_date)

        active_version = self.registry.get_active_version("ARV_ESTIMATION")
        self.assertEqual(active_version.version_id, new_version.version_id)

        # 3. Propose and deploy a second version
        proposal2 = ModelImprovementProposal(target_model="ARV_ESTIMATION", recommendation="Further tuning", supporting_deal_id="deal-002", error_analysis="")
        version2 = self.registry.propose_new_version(proposal2)
        version2.status = ModelVersionStatus.EVALUATING
        self.registry.deploy_version(version2.version_id)

        # Verify the old version is now archived
        self.assertEqual(new_version.status, ModelVersionStatus.ARCHIVED)
        # Verify the new version is active
        self.assertEqual(version2.status, ModelVersionStatus.ACTIVE)
        self.assertEqual(self.registry.get_active_version("ARV_ESTIMATION").version_id, version2.version_id)

    def test_model_rollback(self):
        """PHASE 38: Verify the rollback functionality."""
        # Create and deploy two versions as in the previous test
        v1 = self.registry.propose_new_version(ModelImprovementProposal(target_model="ARV_ESTIMATION", recommendation="v1", supporting_deal_id="d1", error_analysis=""))
        v1.status = ModelVersionStatus.EVALUATING
        self.registry.deploy_version(v1.version_id)

        v2 = self.registry.propose_new_version(ModelImprovementProposal(target_model="ARV_ESTIMATION", recommendation="v2", supporting_deal_id="d2", error_analysis=""))
        v2.status = ModelVersionStatus.EVALUATING
        self.registry.deploy_version(v2.version_id)

        self.assertEqual(self.registry.get_active_version("ARV_ESTIMATION").version_id, v2.version_id)

        # Now, roll back to v1
        rolled_back = self.registry.rollback_to_version(v1.version_id)
        self.assertTrue(rolled_back)
        self.assertEqual(self.registry.get_active_version("ARV_ESTIMATION").version_id, v1.version_id)
        self.assertEqual(v2.status, ModelVersionStatus.ARCHIVED)