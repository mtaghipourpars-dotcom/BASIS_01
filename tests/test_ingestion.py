import unittest
from copy import deepcopy

from app.ingestion import ObservationStore


METRIC = {
    "schema_version": "1.0",
    "record_type": "metric",
    "record_id": "demo-host-cpu-001",
    "environment": "DEMO",
    "target": {"system_id": "S4D", "component": "host"},
    "metric": {"id": "host.cpu.utilization", "value": 42.7, "unit": "percent"},
    "source": {"adapter_id": "demo-fixture", "adapter_version": "0.1.0", "source_type": "DEMO_FIXTURE"},
    "observed_at": "2026-10-17T20:00:00Z",
    "received_at": "2026-10-17T20:00:02Z",
    "quality": {"status": "VALID", "freshness": "FRESH", "flags": []},
    "evidence_ref": "demo-evidence-001",
}


class IngestionTests(unittest.TestCase):
    def setUp(self):
        self.store = ObservationStore()

    def tearDown(self):
        self.store.close()

    def test_first_record_is_inserted(self):
        self.assertEqual(self.store.ingest(METRIC), "INSERTED")

    def test_same_payload_is_idempotent(self):
        self.assertEqual(self.store.ingest(METRIC), "INSERTED")
        self.assertEqual(self.store.ingest(deepcopy(METRIC)), "DUPLICATE")
        self.assertEqual(self.store.conflict_count(), 0)

    def test_conflicting_payload_is_retained_as_conflict_not_overwritten(self):
        self.store.ingest(METRIC)
        changed = deepcopy(METRIC)
        changed["metric"]["value"] = 99.0
        self.assertEqual(self.store.ingest(changed), "CONFLICT")
        self.assertEqual(self.store.get(METRIC["record_id"])["metric"]["value"], 42.7)
        self.assertEqual(self.store.conflict_count(METRIC["record_id"]), 1)


if __name__ == "__main__":
    unittest.main()
