import os
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from inneros_act3.evolus_adapter import (
    EvolusWorkOrder,
    KnowledgeReference,
    WorkOrderStep,
    evolus_smoke,
    execute_workflow,
    get_evolus_config,
    get_evolus_credential,
    query_knowledge_library,
)


class EvolusAdapterTests(unittest.TestCase):
    def test_query_knowledge_library_mock(self):
        context = {"incident_id": "INC-TEST-EV", "node": "intel-primary"}
        k_refs = query_knowledge_library("link failover", context, mock=True)
        self.assertIsInstance(k_refs, tuple)
        self.assertTrue(len(k_refs) >= 2)
        first = k_refs[0]
        self.assertIsInstance(first, KnowledgeReference)
        self.assertTrue(first.article_id.startswith("SOP-"))
        self.assertTrue(first.relevance_score > 0.5)
        self.assertTrue(len(first.policy_code) > 0)

    def test_execute_workflow_mock(self):
        plan = {
            "incident_id": "INC-TEST-EV",
            "category": "network",
            "diagnosis": "Switch port flapped 20 times in 1 min",
        }
        k_refs = query_knowledge_library("link flap", plan, mock=True)
        order = execute_workflow(plan, k_refs, mock=True)

        self.assertIsInstance(order, EvolusWorkOrder)
        self.assertEqual(order.incident_id, "INC-TEST-EV")
        self.assertEqual(order.building_blocks_used, ("workflow", "knowledge_library"))
        self.assertTrue(len(order.steps) >= 2)
        self.assertIsInstance(order.steps[0], WorkOrderStep)
        self.assertTrue(len(order.sha256()) == 64)
        self.assertIn("developer.amd.com.cn", order.model_endpoint)

    def test_work_order_hash_is_deterministic(self):
        plan = {"incident_id": "INC-HASH-TEST"}
        k_refs = query_knowledge_library("query", plan, mock=True)
        o1 = execute_workflow(plan, k_refs, mock=True)
        self.assertEqual(o1.sha256(), o1.sha256())

    def test_evolus_smoke_mock(self):
        report = evolus_smoke(mock=True)
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["eligibility"], "YES")
        self.assertEqual(report["track"], "evolus_act3_partner")
        self.assertIn("workflow", report["building_blocks"])
        self.assertIn("knowledge_library", report["building_blocks"])
        self.assertTrue(report["steps_count"] >= 2)

    def test_evolus_smoke_live_blocked_when_no_key(self):
        old_key = os.environ.get("EVOLUS_API_KEY")
        try:
            os.environ.pop("EVOLUS_API_KEY", None)
            key, _ = get_evolus_credential()
            if not key:
                report = evolus_smoke(mock=False)
                self.assertEqual(report["status"], "BLOCKED")
                self.assertEqual(report["eligibility"], "NO_CREDENTIAL_BLOCKED")
                self.assertIn("EVOLUS_API_KEY", report["required_env_vars"])
                self.assertIn("EVOLUS_WORKSPACE_ID", report["required_env_vars"])
                self.assertIn("EVOLUS_WORKFLOW_ID", report["required_env_vars"])
                self.assertIn("EVOLUS_KNOWLEDGE_LIBRARY_ID", report["required_env_vars"])
        finally:
            if old_key is not None:
                os.environ["EVOLUS_API_KEY"] = old_key


if __name__ == "__main__":
    unittest.main()
