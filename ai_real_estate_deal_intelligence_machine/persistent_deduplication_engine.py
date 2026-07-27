from __future__ import annotations

from .db_client import DatabaseClient


class PersistentDeduplicationEngine:
    """
    A deduplication engine that uses a DatabaseClient for persistence,
    ensuring that fingerprints survive across application restarts.
    """

    def __init__(self, db_client: DatabaseClient):
        self.db_client = db_client

    def is_duplicate(self, fingerprint: str, market_id: str) -> bool:
        """Checks the database to see if a fingerprint already exists for the market."""
        return self.db_client.has_fingerprint(fingerprint, market_id)

    def add(self, fingerprint: str, market_id: str):
        """Adds a fingerprint for the given market to the database."""
        self.db_client.add_fingerprint(fingerprint, market_id)
