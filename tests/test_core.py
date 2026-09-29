import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from inneros_act3.core import RouteRequest, route, verify_evidence
from inneros_act3.evidence import (
    EvidenceBundle,
    ExecutionEvidence,
    HumanTimeReturned,
    RuntimeIdentity,
    sha256_text,
)


class RouterTests(unittest.TestCase):
    def test_privacy_forces_local(self):
        result = route(RouteRequest(privacy_required=True))
        self.assertEqual(result.target, "amd-local")
        self.assertIn("privacy", result.reason_codes)

    def test_elastic_capacity_prefers_cloud(self):
        result = route(RouteRequest(needs_elastic_capacity=True))
        self.assertEqual(result.target, "amd-cloud")
        self.assertIn("capability", result.reason_codes)

    def test_local_first_default(self):
        result = route(RouteRequest())
        self.assertEqual(result.target, "amd-local")
        self.assertIn("local_first", result.reason_codes)

    def test_cloud_fallback(self):
        result = route(RouteRequest(local_available=False, cloud_available=True))
        self.assertEqual(result.target, "amd-cloud")
        self.assertIn("fallback", result.reason_codes)

    def test_privacy_fails_closed(self):
        with self.assertRaises(RuntimeError):
            route(RouteRequest(privacy_required=True, local_available=False))

    def test_evidence_hash_verifies(self):
        result = route(RouteRequest(latency_sensitive=True))
        digest = result.sha256()
        self.assertTrue(verify_evidence(result, digest))
        self.assertFalse(verify_evidence(result, "0" * 64))


class ExecutionEvidenceTests(unittest.TestCase):
    def _execution(self):
        runtime = RuntimeIdentity(
            target="amd-local",
            provider="InnerOS",
            accelerator="AMD Radeon AI PRO R9700",
            architecture="gfx1201",
            runtime="ROCm",
            model="Qwen",
        )
        return ExecutionEvidence(
            run_id="run-1",
            task_id="task-1",
            route_target="amd-local",
            route_reasons=("local_first", "privacy"),
            runtime=runtime,
            started_at="2026-09-28T00:00:00+00:00",
            elapsed_ms=1250.0,
            success=True,
            output_sha256=sha256_text("result"),
            human_time=HumanTimeReturned(600.0, 60.0),
        )

    def test_execution_hash_is_deterministic(self):
        self.assertEqual(self._execution().sha256(), self._execution().sha256())

    def test_bundle_manifest_verifies(self):
        bundle = EvidenceBundle(
            schema="inneros.act3.evidence.v1",
            created_at="2026-09-28T00:00:00+00:00",
            executions=(self._execution(),),
        )
        manifest = bundle.manifest()
        self.assertEqual(len(manifest["bundle_sha256"]), 64)
        self.assertTrue(bundle.verify())

    def test_human_time_returned(self):
        metric = HumanTimeReturned(600.0, 60.0)
        self.assertEqual(metric.returned_seconds, 540.0)
        self.assertAlmostEqual(metric.automation_rate, 0.9)

    def test_human_time_never_goes_negative(self):
        metric = HumanTimeReturned(60.0, 90.0)
        self.assertEqual(metric.returned_seconds, 0.0)
        self.assertEqual(metric.automation_rate, 0.0)


class DemoBundleTests(unittest.TestCase):
    def test_demo_bundle_is_verifiable_and_truthful(self):
        from inneros_act3.demo import build_demo_bundle

        bundle = build_demo_bundle()
        self.assertTrue(bundle.verify())
        self.assertEqual(len(bundle.executions), 4)
        states = {item.runtime.target: item.runtime.truth_state for item in bundle.executions}
        self.assertEqual(states["amd-local"], "PROVEN")
        self.assertEqual(states["amd-cloud"], "CONTRACT-ONLY")
        self.assertTrue(all(item.human_time.source == "ESTIMATED" for item in bundle.executions))


if __name__ == "__main__":
    unittest.main()
