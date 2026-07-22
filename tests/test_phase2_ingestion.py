import unittest

from ai_real_estate_deal_intelligence_machine.phase2 import (
    CSVImportProvider,
    IngestionEvent,
    IngestionEngine,
    ProviderStatus,
    ProviderSyncSchedule,
    ProviderRegistry,
)


class Phase2IngestionTests(unittest.TestCase):
    def test_provider_status_has_expected_states(self):
        status_values = {status.value for status in ProviderStatus}
        self.assertTrue({"ONLINE", "OFFLINE", "DEGRADED", "RATE_LIMITED", "ERROR"}.issubset(status_values))

    def test_ingestion_engine_handles_mock_and_csv_records(self):
        engine = IngestionEngine()
        records = engine.ingest_sample_data()

        self.assertGreaterEqual(len(records), 1)
        self.assertTrue(all(record["normalized"] for record in records))
        self.assertTrue(all(record["deduplicated"] for record in records))
        self.assertTrue(all(record["confidence_score"] >= 0 for record in records))

    def test_csv_provider_is_available_and_emits_events(self):
        provider = CSVImportProvider("tests/sample_property_data.csv")
        events = provider.fetch_records()

        self.assertGreaterEqual(len(events), 1)
        self.assertTrue(all(event.event_type == "NEW_RECORD_RECEIVED" for event in events))

    def test_provider_registry_and_schedule_foundation_exist(self):
        registry = ProviderRegistry()
        schedule = ProviderSyncSchedule()

        self.assertGreaterEqual(len(registry.providers), 1)
        self.assertTrue(schedule.interval_minutes >= 1)


if __name__ == "__main__":
    unittest.main()
