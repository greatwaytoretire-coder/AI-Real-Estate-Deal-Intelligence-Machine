import unittest
from pathlib import Path

from ai_real_estate_deal_intelligence_machine.audit_logger import AuditLogger
from ai_real_estate_deal_intelligence_machine.phase28 import (
    AutonomyLevel,
    ReliabilityEngine,
    SafetyControls,
    SystemState,
)


class Phase28HardeningTest(unittest.TestCase):
    def setUp(self):
        self.log_path = Path("data/test_phase28_audit.log")
        self.log_path.unlink(missing_ok=True)
        self.audit_logger = AuditLogger(log_path=self.log_path)
        self.system_state = SystemState(audit_logger=self.audit_logger)

    def tearDown(self):
        self.log_path.unlink(missing_ok=True)

    def test_emergency_stop_and_autonomy_levels(self):
        """
        PHASE 28: Verify emergency stop halts actions and autonomy levels are respected.
        """
        safety = SafetyControls(self.system_state)

        # Check that a safe action is allowed by default
        self.assertTrue(safety.check("TEST_ACTION", "user-123", AutonomyLevel.HUMAN_IN_THE_LOOP))

        # Activate emergency stop
        self.system_state.activate_emergency_stop("operator-greg", "System instability detected.")
        self.assertTrue(self.system_state.emergency_stop_activated)

        # Verify action is now blocked
        self.assertFalse(safety.check("TEST_ACTION", "user-123", AutonomyLevel.HUMAN_IN_THE_LOOP))

        # Deactivate emergency stop
        self.system_state.deactivate_emergency_stop("operator-greg", "System stabilized.")
        self.assertFalse(self.system_state.emergency_stop_activated)

        # Verify action is allowed again
        self.assertTrue(safety.check("TEST_ACTION", "user-123", AutonomyLevel.HUMAN_IN_THE_LOOP))

        # Verify autonomy level check
        self.assertFalse(safety.check("TEST_ACTION", "user-123", AutonomyLevel.CONTROLLED_AUTONOMY))

    def test_reliability_engine_retries_and_dlq(self):
        """
        PHASE 28: Verify job retries with backoff and dead-letter queue handling.
        """
        engine = ReliabilityEngine(self.system_state, max_retries=2)

        # Submit a job that will fail twice then succeed
        job_id = "job-transient-failure"
        engine.submit_job(job_id, {"data": "important"})

        # Simulate failure on attempt 1
        engine.process_queue(failure_simulation={"job_id": job_id, "fail_attempts": 1})
        self.assertEqual(len(engine.job_queue), 1)
        self.assertEqual(engine.job_queue[0].attempts, 1)

        # Simulate success on attempt 2
        engine.process_queue(failure_simulation={"job_id": job_id, "fail_attempts": 1})
        self.assertEqual(len(engine.job_queue), 0)
        self.assertIn(job_id, engine.processed_ids)

        # Submit a job that will fail permanently
        job_id_perm = "job-permanent-failure"
        engine.submit_job(job_id_perm, {"data": "critical"})

        # Fail it more than max_retries
        engine.process_queue(failure_simulation={"job_id": job_id_perm, "fail_attempts": 3})  # Fails attempt 1
        engine.process_queue(failure_simulation={"job_id": job_id_perm, "fail_attempts": 3})  # Fails attempt 2

        # It should now be in the DLQ
        self.assertEqual(len(engine.job_queue), 0)
        self.assertEqual(len(engine.dead_letter_queue), 1)
        self.assertEqual(engine.dead_letter_queue[0].job_id, job_id_perm)

    def test_idempotency_prevents_duplicate_processing(self):
        """
        PHASE 28: Verify that duplicate jobs are not processed.
        """
        engine = ReliabilityEngine(self.system_state)
        job_id = "job-idempotent"

        # Submit and process once
        self.assertTrue(engine.submit_job(job_id, {"data": "once"}))
        engine.process_queue()
        self.assertIn(job_id, engine.processed_ids)

        # Submit again, should be ignored
        self.assertFalse(engine.submit_job(job_id, {"data": "twice"}))
        self.assertEqual(len(engine.job_queue), 0)