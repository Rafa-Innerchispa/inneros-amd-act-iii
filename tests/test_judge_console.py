from __future__ import annotations

import json
import unittest

from inneros_act3.judge_console import (
    VERIFIED_RECEIPT,
    _assert_no_secret_material,
    build_status_payload,
    run_demo,
)


class JudgeConsoleTests(unittest.TestCase):
    def test_status_exposes_verified_receipt_without_secret(self):
        status = build_status_payload()
        self.assertEqual(status["status"], "READY")
        self.assertEqual(status["last_verified"]["truth"], "LIVE_VERIFIED_REPLAY")
        _assert_no_secret_material(status)

    def test_replay_is_live_verified_but_explicitly_replay(self):
        payload = run_demo("replay")
        self.assertEqual(payload["truth"], "LIVE_VERIFIED_REPLAY")
        self.assertTrue(payload["pipeline"]["evidence"]["verified"])
        self.assertEqual(payload["pipeline"]["gemma"]["model"], "Gemma-4-31B-IT")
        self.assertEqual(payload["pipeline"]["evolus"]["building_blocks"], ["workflow", "knowledge_library"])
        _assert_no_secret_material(payload)

    def test_mock_never_claims_live(self):
        payload = run_demo("mock")
        self.assertEqual(payload["truth"], "MOCK")
        self.assertTrue(payload["pipeline"]["evidence"]["verified"])
        self.assertEqual(payload["pipeline"]["gemma"]["status"], "MOCK")
        self.assertEqual(payload["pipeline"]["evolus"]["status"], "MOCK")
        _assert_no_secret_material(payload)

    def test_receipt_has_expected_verified_evidence(self):
        self.assertEqual(
            VERIFIED_RECEIPT["pipeline"]["evidence"]["bundle_sha256"],
            "6ee36d6905929b176fd9c49f3c1a4aa165df4a8231d5047871f581eb73b3f845",
        )
        self.assertEqual(VERIFIED_RECEIPT["pipeline"]["evolus"]["application_name"], "InnerOS")

    def test_public_payload_does_not_name_secret_fields(self):
        dumped = json.dumps(VERIFIED_RECEIPT).lower()
        self.assertNotIn('"api_key"', dumped)
        self.assertNotIn('"authorization"', dumped)
        self.assertNotIn('"secret"', dumped)


if __name__ == "__main__":
    unittest.main()
