import unittest
from pathlib import Path

from .db_client import DatabaseClient
from .persistent_deduplication_engine import PersistentDeduplicationEngine


class PersistentDeduplicationEngineTest(unittest.TestCase):
    def setUp(self):
        """Set up a temporary database for each test."""
        self.db_path = Path("data/test_persistent_dedup.db")
        self.db_path.unlink(missing_ok=True)
        self.db_client = DatabaseClient(database_path=self.db_path)
        self.engine = PersistentDeduplicationEngine(db_client=self.db_client)

    def tearDown(self):
        """Clean up the temporary database after each test."""
        self.db_client.close()
        self.db_path.unlink(missing_ok=True)

    def test_add_and_check_fingerprint(self):
        """Verify a fingerprint can be added and checked for duplicates."""
        fingerprint = "fp_test_001"
        market_id = "market_A"

        # Initially, it's not a duplicate
        self.assertFalse(self.engine.is_duplicate(fingerprint, market_id))

        # Add the fingerprint
        self.engine.add(fingerprint, market_id)

        # Now it should be a duplicate
        self.assertTrue(self.engine.is_duplicate(fingerprint, market_id))

        # Verify it's not a duplicate in a different market
        self.assertFalse(self.engine.is_duplicate(fingerprint, "market_B"))

    def test_fingerprint_persists_across_restarts(self):
        """
        Verify that deduplication fingerprints survive a simulated process restart.
        """
        fingerprint = "fp_persistent_002"
        market_id = "market_persistent"

        # 1. Add a fingerprint and verify it exists
        self.engine.add(fingerprint, market_id)
        self.assertTrue(self.engine.is_duplicate(fingerprint, market_id))

        # 2. Simulate a restart by closing the DB and creating new clients
        self.db_client.close()

        with DatabaseClient(database_path=self.db_path) as new_db_client:
            new_engine = PersistentDeduplicationEngine(db_client=new_db_client)

            # 3. Verify the fingerprint still exists in the new engine instance
            self.assertTrue(new_engine.is_duplicate(fingerprint, market_id))

            # 4. Verify cross-market isolation is also preserved
            self.assertFalse(new_engine.is_duplicate(fingerprint, "other_market"))