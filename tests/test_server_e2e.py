from __future__ import annotations

import http.client
import json
import threading
import time
import unittest
from urllib.parse import urlparse

from inneros_act3.access import (
    AccessManager,
    RateLimiter,
    SESSION_COOKIE,
    hash_password,
)
from inneros_act3.server import create_server


class ServerE2ETests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.port = 8799
        cls.test_password = "ServerE2EPwd2026!Clean"
        cls.mgr = AccessManager(
            session_secret="test_server_e2e_secret_2026_xyz",
            judge_user="amd-judge",
            judge_password_hash=hash_password(cls.test_password),
            session_ttl_seconds=3600,
            rate_limiter=RateLimiter(max_attempts=10, window_seconds=60),
        )
        cls.server = create_server("127.0.0.1", cls.port, cls.mgr)
        cls.server_thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.server_thread.start()
        time.sleep(0.1)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.server.shutdown()
        cls.server.server_close()

    def _get(self, path: str, cookie: str | None = None) -> tuple[int, dict[str, str], bytes]:
        conn = http.client.HTTPConnection("127.0.0.1", self.port)
        headers = {}
        if cookie:
            headers["Cookie"] = cookie
        conn.request("GET", path, headers=headers)
        resp = conn.getresponse()
        data = resp.read()
        resp_headers = {k.lower(): v for k, v in resp.getheaders()}
        conn.close()
        return resp.status, resp_headers, data

    def _post(self, path: str, form_data: str, cookie: str | None = None) -> tuple[int, dict[str, str], bytes]:
        conn = http.client.HTTPConnection("127.0.0.1", self.port)
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        if cookie:
            headers["Cookie"] = cookie
        conn.request("POST", path, body=form_data, headers=headers)
        resp = conn.getresponse()
        data = resp.read()
        resp_headers = {k.lower(): v for k, v in resp.getheaders()}
        conn.close()
        return resp.status, resp_headers, data

    def test_01_public_health_endpoint(self) -> None:
        status, headers, data = self._get("/health")
        self.assertEqual(status, 200)
        self.assertIn("application/json", headers.get("content-type", ""))
        payload = json.loads(data.decode("utf-8"))
        self.assertEqual(payload["status"], "healthy")
        self.assertEqual(payload["segment"], "judge_act3")
        self.assertEqual(payload["service"], "inneros-act3")
        self.assertEqual(payload["auth"], "inneros_access_v1")

    def test_02_login_page_renders_cleanly(self) -> None:
        status, headers, data = self._get("/login")
        self.assertEqual(status, 200)
        self.assertIn("text/html", headers.get("content-type", ""))
        html = data.decode("utf-8")
        self.assertIn("InnerOS", html)
        self.assertIn("Access", html)
        self.assertIn("judge_act3", html)
        self.assertIn('name="username"', html)
        self.assertIn('name="password"', html)

    def test_03_unauthenticated_console_redirects_to_login(self) -> None:
        status, headers, _ = self._get("/")
        self.assertEqual(status, 302)
        loc = headers.get("location", "")
        self.assertTrue(loc.startswith("/login?next="))

    def test_04_unauthenticated_api_returns_401(self) -> None:
        status, headers, data = self._get("/api/status")
        self.assertEqual(status, 401)
        payload = json.loads(data.decode("utf-8"))
        self.assertFalse(payload.get("ok"))
        self.assertEqual(payload.get("error"), "unauthorized")

    def test_05_failed_login_returns_401_with_alert(self) -> None:
        status, headers, data = self._post("/login", "username=amd-judge&password=WrongPassword")
        self.assertEqual(status, 401)
        html = data.decode("utf-8")
        self.assertIn("Credenciales no válidas", html)

    def test_06_successful_login_sets_session_cookie_and_redirects(self) -> None:
        form = f"username=amd-judge&password={self.test_password}&next=%2F"
        status, headers, _ = self._post("/login", form)
        self.assertEqual(status, 302)
        self.assertEqual(headers.get("location"), "/")
        set_cookie = headers.get("set-cookie", "")
        self.assertIn(f"{SESSION_COOKIE}=", set_cookie)
        self.assertIn("HttpOnly", set_cookie)
        self.assertIn("SameSite=Lax", set_cookie)

    def test_07_authenticated_session_accesses_console_and_apis(self) -> None:
        # 1. Login to get cookie
        form = f"username=amd-judge&password={self.test_password}&next=%2F"
        _, headers, _ = self._post("/login", form)
        raw_cookie = headers.get("set-cookie", "").split(";")[0]

        # 2. Access Console UI
        status, _, data = self._get("/", cookie=raw_cookie)
        self.assertEqual(status, 200)
        self.assertIn("InnerOS", data.decode("utf-8"))

        # 3. Access Protected API Status
        status, _, data = self._get("/api/status", cookie=raw_cookie)
        self.assertEqual(status, 200)
        status_payload = json.loads(data.decode("utf-8"))
        self.assertEqual(status_payload["status"], "READY")

        # 4. Access Protected API Me
        status, _, data = self._get("/api/me", cookie=raw_cookie)
        self.assertEqual(status, 200)
        me_payload = json.loads(data.decode("utf-8"))
        self.assertTrue(me_payload["ok"])
        self.assertEqual(me_payload["principal"]["role"], "judge_act3")
        self.assertEqual(me_payload["principal"]["username"], "amd-judge")

    def test_08_logout_clears_cookie_and_redirects(self) -> None:
        status, headers, _ = self._get("/logout")
        self.assertEqual(status, 302)
        self.assertEqual(headers.get("location"), "/login")
        set_cookie = headers.get("set-cookie", "")
        self.assertIn(f"{SESSION_COOKIE}=", set_cookie)
        self.assertIn("Max-Age=0", set_cookie)

    def test_09_tampered_cookie_redirects_to_login(self) -> None:
        tampered_cookie = f"{SESSION_COOKIE}=fake_token.bad_signature"
        status, headers, _ = self._get("/", cookie=tampered_cookie)
        self.assertEqual(status, 302)
        self.assertTrue(headers.get("location", "").startswith("/login"))


if __name__ == "__main__":
    unittest.main()
