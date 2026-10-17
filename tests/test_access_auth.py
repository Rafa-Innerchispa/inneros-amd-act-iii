from __future__ import annotations

import time
import unittest

from inneros_act3.access import (
    AccessManager,
    AuthPrincipal,
    RateLimiter,
    SESSION_COOKIE,
    hash_password,
    verify_password,
)


class AccessAuthTests(unittest.TestCase):
    def setUp(self) -> None:
        self.test_password = "TestEvaluatorPassphrase2026!"
        self.mgr = AccessManager(
            session_secret="test_secret_key_inneros_access_2026",
            judge_user="amd-judge",
            judge_password_hash=hash_password(self.test_password),
            session_ttl_seconds=3600,
            rate_limiter=RateLimiter(max_attempts=3, window_seconds=10),
        )

    def test_valid_login(self) -> None:
        principal, err = self.mgr.authenticate("amd-judge", self.test_password)
        self.assertIsNone(err)
        self.assertIsNotNone(principal)
        self.assertEqual(principal.username, "amd-judge")
        self.assertEqual(principal.role, "judge_act3")
        self.assertEqual(principal.segment, "judge_act3")
        self.assertEqual(principal.auth_source, "judge_credentials")

    def test_invalid_login(self) -> None:
        principal, err = self.mgr.authenticate("amd-judge", "WrongPassword!999")
        self.assertIsNone(principal)
        self.assertEqual(err, "invalid_credentials")

    def test_unknown_user(self) -> None:
        principal, err = self.mgr.authenticate("unknown-user", self.test_password)
        self.assertIsNone(principal)
        self.assertEqual(err, "invalid_credentials")

    def test_empty_credentials(self) -> None:
        p1, err1 = self.mgr.authenticate("", "somepass")
        p2, err2 = self.mgr.authenticate("amd-judge", "")
        self.assertIsNone(p1)
        self.assertIsNone(p2)
        self.assertEqual(err1, "invalid_credentials")
        self.assertEqual(err2, "invalid_credentials")

    def test_session_lifecycle(self) -> None:
        principal, _ = self.mgr.authenticate("amd-judge", self.test_password)
        self.assertIsNotNone(principal)
        token = self.mgr.issue_session(principal)
        self.assertIn(".", token)

        # Verify from cookie header
        cookie_header = f"foo=bar; {SESSION_COOKIE}={token}; baz=qux"
        extracted = self.mgr.extract_session_token(cookie_header)
        self.assertEqual(extracted, token)

        verified = self.mgr.verify_session_token(token)
        self.assertIsNotNone(verified)
        self.assertEqual(verified.username, "amd-judge")
        self.assertEqual(verified.role, "judge_act3")
        self.assertEqual(verified.segment, "judge_act3")

    def test_tampered_cookie_rejected(self) -> None:
        principal, _ = self.mgr.authenticate("amd-judge", self.test_password)
        token = self.mgr.issue_session(principal)
        tampered = token[:-4] + "xxxx"
        self.assertIsNone(self.mgr.verify_session_token(tampered))

        # Tampered body
        body, sig = token.split(".", 1)
        tampered_body = body[:-2] + "AA"
        self.assertIsNone(self.mgr.verify_session_token(f"{tampered_body}.{sig}"))

    def test_expired_cookie_rejected(self) -> None:
        principal = AuthPrincipal(
            subject="judge:amd-judge",
            username="amd-judge",
            role="judge_act3",
            segment="judge_act3",
            display_name="AMD ACT III Judge",
            auth_source="test",
            issued_at=int(time.time()) - 200,
            expires_at=int(time.time()) - 5,  # expired 5 seconds ago
        )
        token = self.mgr.issue_session(principal)
        self.assertIsNone(self.mgr.verify_session_token(token))

    def test_rate_limiting(self) -> None:
        ip = "192.168.1.100"
        # 3 failed attempts allowed
        for _ in range(3):
            p, err = self.mgr.authenticate("amd-judge", "badpass", client_ip=ip)
            self.assertEqual(err, "invalid_credentials")

        # 4th attempt blocked by rate limiter even with valid credentials
        p, err = self.mgr.authenticate("amd-judge", self.test_password, client_ip=ip)
        self.assertIsNone(p)
        self.assertEqual(err, "rate_limited")

    def test_password_hashing(self) -> None:
        pwd = "TestSecretPassword123!"
        hashed = hash_password(pwd)
        self.assertTrue(hashed.startswith("pbkdf2_sha256$260000$"))
        self.assertTrue(verify_password(pwd, hashed))
        self.assertFalse(verify_password("wrong", hashed))


if __name__ == "__main__":
    unittest.main()
