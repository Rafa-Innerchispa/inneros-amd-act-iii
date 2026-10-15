from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from inneros_act3.dual_prize import DualPrizeResult, run_dual_prize_pipeline
from inneros_act3.smoke import main as smoke_main


class DualPrizePipelineTests(unittest.TestCase):
    def test_run_dual_prize_pipeline_mock(self):
        incident = {
            "incident_id": "INC-BELLINI-UNIT-01",
            "title": "Edge Gateway Optic Failure",
            "loss_of_carrier": True,
            "category": "network",
            "telemetry": {"latency_ms": 320},
        }
        res = run_dual_prize_pipeline(incident, gemma_mock=True, evolus_mock=True)

        self.assertIsInstance(res, DualPrizeResult)
        self.assertEqual(res.incident_id, "INC-BELLINI-UNIT-01")
        self.assertEqual(res.eligibility_google_gemma, "YES")
        self.assertEqual(res.eligibility_evolus, "YES")

        # Gemma Plan
        self.assertEqual(res.gemma_plan.incident_id, "INC-BELLINI-UNIT-01")
        self.assertEqual(res.gemma_plan.severity, "critical")
        self.assertEqual(res.gemma_plan.delegation_lane, "evolus_business_flow")

        # Evolus Work Order
        self.assertTrue(res.evolus_work_order.work_order_id.startswith("WO-EVOLUS-"))
        self.assertEqual(res.evolus_work_order.building_blocks_used, ("workflow", "knowledge_library"))
        self.assertTrue(len(res.evolus_work_order.steps) >= 2)

        # Evidence Bundle
        self.assertEqual(len(res.evidence_bundle.executions), 2)
        targets = {e.runtime.target for e in res.evidence_bundle.executions}
        self.assertEqual(targets, {"amd-cloud"})
        self.assertTrue(res.evidence_bundle.verify())

        # Human Time Returned
        htr = res.human_time_returned
        self.assertEqual(htr.baseline_manual_seconds, 2700.0)
        self.assertEqual(htr.active_human_seconds, 120.0)
        self.assertEqual(htr.returned_seconds, 2580.0)
        self.assertAlmostEqual(htr.automation_rate, 2580.0 / 2700.0, places=4)

        # Manifest
        manifest = res.manifest()
        self.assertEqual(manifest["schema"], "inneros.act3.dual-prize.v1")
        self.assertEqual(manifest["google_gemma"]["eligibility"], "YES")
        self.assertEqual(manifest["evolus"]["eligibility"], "YES")
        self.assertTrue(len(manifest["bundle_sha256"]) == 64)

    def test_smoke_cli_runner_all_mock(self):
        exit_code = smoke_main(["--all", "--json"])
        self.assertEqual(exit_code, 0)

    def test_smoke_cli_runner_individual_flags(self):
        self.assertEqual(smoke_main(["--gemma", "--json"]), 0)
        self.assertEqual(smoke_main(["--evolus", "--json"]), 0)
        self.assertEqual(smoke_main(["--dual", "--json"]), 0)

    def test_smoke_cli_runner_live_mode_blocked_graceful(self):
        exit_code = smoke_main(["--all", "--live", "--json"])
        self.assertEqual(exit_code, 0)


if __name__ == "__main__":
    unittest.main()
