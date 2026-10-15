import os
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from inneros_act3.token_factory_provider import (
    DEFAULT_TOKEN_FACTORY_MODEL,
    IncidentAction,
    IncidentPlan,
    generate_incident_plan,
    get_token_factory_credential,
    is_token_factory_enabled,
    list_token_factory_models,
    token_factory_smoke,
    validate_incident_plan,
)


class TokenFactoryProviderTests(unittest.TestCase):
    def test_list_models_mock(self):
        res = list_token_factory_models(mock=True)
        self.assertEqual(res["object"], "list")
        self.assertTrue(len(res["data"]) >= 1)
        self.assertEqual(res["data"][0]["id"], DEFAULT_TOKEN_FACTORY_MODEL)

    def test_generate_incident_plan_mock(self):
        context = {
            "incident_id": "INC-TEST-001",
            "loss_of_carrier": True,
            "category": "network",
            "telemetry": {"latency_ms": 250},
        }
        plan = generate_incident_plan(context, mock=True)
        self.assertIsInstance(plan, IncidentPlan)
        self.assertEqual(plan.incident_id, "INC-TEST-001")
        self.assertEqual(plan.severity, "critical")
        self.assertEqual(plan.category, "network")
        self.assertTrue(len(plan.recommended_actions) >= 1)
        self.assertEqual(plan.delegation_lane, "evolus_business_flow")
        self.assertEqual(plan.model, DEFAULT_TOKEN_FACTORY_MODEL)
        self.assertTrue(len(plan.sha256()) == 64)

    def test_plan_hash_is_deterministic(self):
        context = {"incident_id": "INC-DET-01", "category": "network"}
        p1 = generate_incident_plan(context, mock=True)
        self.assertEqual(p1.sha256(), p1.sha256())

    def test_validate_plan_rejects_missing_fields(self):
        incomplete = {"incident_id": "INC-FAIL"}
        with self.assertRaises(ValueError):
            validate_incident_plan(incomplete)

    def test_token_factory_safety_toggle(self):
        old_env = os.environ.get("INNEROS_ACT3_TOKEN_FACTORY_ENABLED")
        try:
            os.environ["INNEROS_ACT3_TOKEN_FACTORY_ENABLED"] = "0"
            self.assertFalse(is_token_factory_enabled())
            res = list_token_factory_models(mock=False)
            self.assertEqual(res.get("error"), "token_factory_disabled_by_env")

            with self.assertRaises(RuntimeError):
                generate_incident_plan({"incident_id": "INC-DIS"}, mock=False)
        finally:
            if old_env is not None:
                os.environ["INNEROS_ACT3_TOKEN_FACTORY_ENABLED"] = old_env
            else:
                os.environ.pop("INNEROS_ACT3_TOKEN_FACTORY_ENABLED", None)

    def test_token_factory_smoke_mock(self):
        report = token_factory_smoke(mock=True)
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["eligibility"], "YES")
        self.assertEqual(report["track"], "google_gemma_amd_token_factory")
        self.assertTrue(len(report["plan_sha256"]) == 64)

    def test_token_factory_smoke_live_blocked_when_no_key(self):
        old_key = os.environ.get("AMD_TOKEN_FACTORY_API_KEY")
        try:
            os.environ.pop("AMD_TOKEN_FACTORY_API_KEY", None)
            # If no key in vault, it will report BLOCKED
            key, _ = get_token_factory_credential()
            if not key:
                report = token_factory_smoke(mock=False)
                self.assertEqual(report["status"], "BLOCKED")
                self.assertEqual(report["eligibility"], "NO_CREDENTIAL_BLOCKED")
                self.assertIn("AMD_TOKEN_FACTORY_API_KEY", report["required_env_vars"])
        finally:
            if old_key is not None:
                os.environ["AMD_TOKEN_FACTORY_API_KEY"] = old_key


if __name__ == "__main__":
    unittest.main()
