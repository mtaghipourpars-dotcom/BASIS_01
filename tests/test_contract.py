import unittest
from copy import deepcopy
from datetime import datetime, timezone

from app.contract import ContractError, freshness_state, validate_observation


METRIC = {
    "schema_version": "1.0",
    "record_type": "metric",
    "record_id": "demo-host-cpu-001",
    "environment": "DEMO",
    "target": {"system_id": "S4D", "sid": "S4D", "component": "host"},
    "metric": {"id": "host.cpu.utilization", "value": 0, "unit": "percent"},
    "source": {"adapter_id": "demo-fixture", "adapter_version": "0.1.0", "source_type": "DEMO_FIXTURE"},
    "observed_at": "2026-01-01T10:00:00Z",
    "received_at": "2026-01-01T10:00:02Z",
    "quality": {"status": "VALID", "freshness": "FRESH", "flags": []},
    "evidence_ref": "demo-evidence-001",
}


class ContractTests(unittest.TestCase):
    def test_valid_metric_and_explicit_zero(self):
        validate_observation(METRIC)
        self.assertEqual(METRIC["metric"]["value"], 0)

    def test_missing_value_is_not_zero(self):
        record = deepcopy(METRIC)
        record["metric"].pop("value")
        with self.assertRaisesRegex(ContractError, "must be numeric"):
            validate_observation(record)

    def test_naive_timestamp_rejected(self):
        record = deepcopy(METRIC)
        record["observed_at"] = "2026-01-01T10:00:00"
        with self.assertRaisesRegex(ContractError, "include a timezone"):
            validate_observation(record)

    def test_demo_environment_required_to_be_explicit(self):
        record = deepcopy(METRIC)
        record["environment"] = "LIVE_DEMO"
        with self.assertRaisesRegex(ContractError, "environment"):
            validate_observation(record)

    def test_missing_evidence_rejected(self):
        record = deepcopy(METRIC)
        record["evidence_ref"] = ""
        with self.assertRaisesRegex(ContractError, "evidence_ref"):
            validate_observation(record)

    def test_absent_collection_is_unknown(self):
        now = datetime(2026, 1, 1, 10, tzinfo=timezone.utc)
        self.assertEqual(freshness_state(None, now, 300), "UNKNOWN")

    def test_old_collection_is_stale(self):
        now = datetime(2026, 1, 1, 10, tzinfo=timezone.utc)
        self.assertEqual(freshness_state("2026-01-01T09:00:00Z", now, 300), "STALE")

    def test_future_timestamp_is_unknown(self):
        now = datetime(2026, 1, 1, 10, tzinfo=timezone.utc)
        self.assertEqual(freshness_state("2026-01-01T10:01:00Z", now, 300), "UNKNOWN")


if __name__ == "__main__":
    unittest.main()
