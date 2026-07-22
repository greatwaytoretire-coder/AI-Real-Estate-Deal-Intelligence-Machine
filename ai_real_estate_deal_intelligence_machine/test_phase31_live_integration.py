import os
import unittest
from pathlib import Path

from ai_real_estate_deal_intelligence_machine.audit_logger import AuditLogger
from ai_real_estate_deal_intelligence_machine.phase26 import ProviderManager
from ai_real_estate_deal_intelligence_machine.phase30 import (
    ContinuousRuntime,
    OperatingMode,
)


class Phase31LiveDataIntegrationTest(unittest.TestCase):
    def setUp(self):
        self.log_path = Path("data/test_phase31_audit.log")
        self.log_path.unlink(missing_ok=True)
        self.audit_logger = AuditLogger(log_path=self.log_path)
        if "ATTOM_API_KEY" in os.environ:
            del os.environ["ATTOM_API_KEY"]

    def tearDown(self):
        self.log_path.unlink(missing_ok=True)
        if "ATTOM_API_KEY" in os.environ:
            del os.environ["ATTOM_API_KEY"]

    def test_end_to_end_ingestion_with_mock_fallback(self):
        """
        PHASE 31: Verify the full runtime uses the MOCK provider when no API key is set.
        """
        provider_manager = ProviderManager(audit_logger=self.audit_logger)
        runtime = ContinuousRuntime(audit_logger=self.audit_logger, provider_manager=provider_manager)
        runtime.mode = OperatingMode.PILOT  # A mode that allows live providers if configured

        # Run ingestion for the 'attom' provider
        ingestion_run = runtime.run_ingestion("attom", {"zip": "12345"})

        self.assertEqual(ingestion_run.records_inserted, 1)
        self.assertEqual(len(runtime.job_queue.pending_queue), 1)

        # Verify the log shows the mock provider was used
        with self.log_path.open("r") as f:
            log_contents = f.read()
            self.assertIn("Falling back to MOCK provider: ATTOM API (Mock)", log_contents)

    def test_end_to_end_ingestion_with_live_provider(self):
        """
        PHASE 31: Verify the full runtime uses the LIVE provider when an API key is set.
        """
        os.environ["ATTOM_API_KEY"] = "test-key-is-set"
        provider_manager = ProviderManager(audit_logger=self.audit_logger)
        runtime = ContinuousRuntime(audit_logger=self.audit_logger, provider_manager=provider_manager)
        runtime.mode = OperatingMode.PILOT

        # Run ingestion for the 'attom' provider
        ingestion_run = runtime.run_ingestion("attom", {"zip": "54321"})

        self.assertEqual(ingestion_run.records_inserted, 1)
        self.assertEqual(len(runtime.job_queue.pending_queue), 1)

        # Verify the log shows the live provider was initialized
        with self.log_path.open("r") as f:
            log_contents = f.read()
            self.assertIn("Initialized LIVE provider: ATTOM API", log_contents)

    def test_live_provider_is_blocked_in_mock_mode(self):
        """
        PHASE 31: Verify the runtime safety check prevents using a LIVE provider in MOCK mode.
        """
        os.environ["ATTOM_API_KEY"] = "test-key-is-set"
        provider_manager = ProviderManager(audit_logger=self.audit_logger)
        runtime = ContinuousRuntime(audit_logger=self.audit_logger, provider_manager=provider_manager)
        runtime.mode = OperatingMode.MOCK  # Set to MOCK mode

        # Expect a PermissionError when trying to use a live provider
        with self.assertRaises(PermissionError) as context:
            runtime.run_ingestion("attom", {"zip": "54321"})

        self.assertIn("Cannot use LIVE provider 'attom' in MOCK operating mode", str(context.exception))