from __future__ import annotations

from dataclasses import asdict
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import mimetypes
import os
from pathlib import Path
import sys
from typing import Any
from urllib.parse import parse_qs, quote, unquote, urlparse

from .access import (
    AccessManager,
    AuthPrincipal,
    DEFAULT_JUDGE_HASH,
    DEFAULT_JUDGE_USER,
    SEGMENT_ROUTES,
    SESSION_COOKIE,
)
from .judge_console import (
    DEFAULT_INCIDENT,
    VERIFIED_RECEIPT,
    _assert_no_secret_material,
    build_status_payload,
    run_demo,
)

WEB_ROOT = Path(__file__).with_name("web")
LOGIN_TEMPLATE_PATH = WEB_ROOT / "login.html"


class AccessServerHandler(BaseHTTPRequestHandler):
    server_version = "InnerOSAccess/1.0"
    access_mgr: AccessManager = None  # type: ignore

    def log_message(self, format: str, *args: Any) -> None:
        sys.stderr.write("[inneros-access] " + (format % args) + "\n")

    def _client_ip(self) -> str:
        # Respect Cloudflare headers when running behind Argo Tunnel
        cf_ip = self.headers.get("CF-Connecting-IP")
        if cf_ip:
            return cf_ip.strip()
        xf = self.headers.get("X-Forwarded-For")
        if xf:
            return xf.split(",")[0].strip()
        return self.client_address[0] if self.client_address else "127.0.0.1"

    def _get_principal(self) -> AuthPrincipal | None:
        cookie_header = self.headers.get("Cookie")
        token = self.access_mgr.extract_session_token(cookie_header)
        if not token:
            return None
        return self.access_mgr.verify_session_token(token)

    def _send_json(self, value: Any, status: int = 200, extra_headers: list[tuple[str, str]] | None = None) -> None:
        payload = json.dumps(value, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
        self.send_header("Content-Length", str(len(payload)))
        if extra_headers:
            for k, v in extra_headers:
                self.send_header(k, v)
        self.end_headers()
        self.wfile.write(payload)

    def _send_redirect(self, location: str, extra_headers: list[tuple[str, str]] | None = None) -> None:
        self.send_response(302)
        self.send_header("Location", location)
        self.send_header("Cache-Control", "no-store")
        if extra_headers:
            for k, v in extra_headers:
                self.send_header(k, v)
        self.end_headers()

    def _render_login(self, *, status: int = 200, error_msg: str | None = None, next_path: str = "/", prefill_user: str = "") -> None:
        if LOGIN_TEMPLATE_PATH.exists():
            html = LOGIN_TEMPLATE_PATH.read_text(encoding="utf-8")
        else:
            html = "<h1>InnerOS Access</h1><form method='POST'><input name='username'/><input name='password' type='password'/><button>Login</button></form>"

        alert_html = ""
        if error_msg:
            alert_html = f'<div class="alert"><span aria-hidden="true">⚠️</span><span>{error_msg}</span></div>'

        rendered = (
            html.replace("{{ALERT_SECTION}}", alert_html)
            .replace("{{NEXT_PATH}}", quote(next_path, safe="/?=&-_"))
            .replace("{{PREFILL_USER}}", prefill_user or DEFAULT_JUDGE_USER)
        )
        content = rendered.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def _serve_asset(self, path: Path) -> None:
        resolved = path.resolve()
        if not path.exists() or not path.is_file() or WEB_ROOT.resolve() not in resolved.parents:
            self.send_error(404)
            return
        content = path.read_bytes()
        mime = mimetypes.guess_type(str(path))[0] or "application/octet-stream"
        self.send_response(200)
        self.send_header("Content-Type", mime)
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path

        # 1. Public Health Check
        if path == "/health":
            self._send_json({
                "status": "healthy",
                "service": "inneros-act3",
                "segment": "judge_act3",
                "version": "1.0.0",
                "auth": "inneros_access_v1",
            })
            return

        # 2. Login Page
        if path == "/login":
            principal = self._get_principal()
            qs = parse_qs(parsed.query)
            next_target = qs.get("next", ["/"])[0]
            if principal and principal.role in {"judge_act3", "owner", "admin"}:
                self._send_redirect(next_target if next_target.startswith("/") else "/")
                return
            error_code = qs.get("error", [None])[0]
            error_msg = None
            if error_code == "unauthorized":
                error_msg = "Please log in to access the Judge Console."
            elif error_code == "expired":
                error_msg = "Your evaluation session has expired. Please authenticate again."
            self._render_login(next_path=next_target, error_msg=error_msg)
            return

        # 3. Logout
        if path == "/logout":
            clear_cookie = (
                f"{SESSION_COOKIE}=; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=0"
            )
            self._send_redirect("/login", extra_headers=[("Set-Cookie", clear_cookie)])
            return

        # 4. Protected Routes
        principal = self._get_principal()
        if not principal or principal.role not in {"judge_act3", "owner", "admin"}:
            if path.startswith("/api/"):
                self._send_json({"ok": False, "error": "unauthorized", "login_url": "/login"}, status=401)
                return
            redirect_to = f"/login?next={quote(self.path, safe='')}"
            self._send_redirect(redirect_to)
            return

        # Authenticated requests
        if path in {"/", "/index.html"}:
            self._serve_asset(WEB_ROOT / "index.html")
            return
        if path == "/api/status":
            self._send_json(build_status_payload())
            return
        if path == "/api/replay":
            self._send_json(VERIFIED_RECEIPT)
            return
        if path == "/api/me":
            self._send_json({"ok": True, "principal": principal.to_dict()})
            return
        if path == "/api/health":
            self._send_json({"ok": True, "service": "inneros-act3-judge-console", "segment": principal.segment})
            return
        if path.startswith("/assets/"):
            relative = path.removeprefix("/assets/")
            self._serve_asset(WEB_ROOT / relative)
            return

        self.send_error(404)

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path

        # 1. Login Submission
        if path == "/login":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8", errors="replace")
            params = parse_qs(body)
            username = params.get("username", [""])[0]
            password = params.get("password", [""])[0]
            next_target = params.get("next", ["/"])[0]
            if not next_target.startswith("/"):
                next_target = "/"

            client_ip = self._client_ip()
            principal, err = self.access_mgr.authenticate(username, password, client_ip=client_ip)

            if err == "rate_limited":
                self._render_login(
                    status=429,
                    error_msg="Demasiados intentos fallidos. Intente nuevamente en 60 segundos.",
                    next_path=next_target,
                    prefill_user=username,
                )
                return

            if not principal:
                self._render_login(
                    status=401,
                    error_msg="Credenciales no válidas. Verifique su usuario y clave de juez.",
                    next_path=next_target,
                    prefill_user=username,
                )
                return

            # Successful login
            token = self.access_mgr.issue_session(principal)
            cookie_val = (
                f"{SESSION_COOKIE}={token}; Path=/; HttpOnly; Secure; SameSite=Lax; "
                f"Max-Age={self.access_mgr.session_ttl_seconds}"
            )
            self._send_redirect(next_target, extra_headers=[("Set-Cookie", cookie_val)])
            return

        # 2. Logout POST
        if path == "/logout":
            clear_cookie = f"{SESSION_COOKIE}=; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=0"
            self._send_redirect("/login", extra_headers=[("Set-Cookie", clear_cookie)])
            return

        # 3. Protected API Endpoints
        principal = self._get_principal()
        if not principal or principal.role not in {"judge_act3", "owner", "admin"}:
            self._send_json({"ok": False, "error": "unauthorized", "login_url": "/login"}, status=401)
            return

        if path == "/api/run":
            mode = parse_qs(parsed.query).get("mode", ["live"])[0]
            try:
                result = run_demo(mode)
                status = 200 if result.get("truth") not in {"BLOCKED", "FAILED"} else 503
                self._send_json(result, status=status)
            except Exception as exc:
                self._send_json(
                    {
                        "mode": mode,
                        "truth": "BLOCKED",
                        "error": type(exc).__name__,
                        "message": str(exc),
                    },
                    status=503,
                )
            return

        self.send_error(404)


def create_server(host: str = "0.0.0.0", port: int = 8789, access_mgr: AccessManager | None = None) -> ThreadingHTTPServer:
    mgr = access_mgr or AccessManager()
    handler = type("ConfiguredAccessHandler", (AccessServerHandler,), {"access_mgr": mgr})
    return ThreadingHTTPServer((host, port), handler)


def main(argv: list[str] | None = None) -> int:
    argv = list(argv or sys.argv[1:])
    host = "0.0.0.0"
    port = 8789
    for item in argv:
        if item.startswith("--host="):
            host = item.split("=", 1)[1]
        elif item.startswith("--port="):
            port = int(item.split("=", 1)[1])

    mgr = AccessManager()
    server = create_server(host, port, mgr)
    print(f"InnerOS Access Server running on http://{host}:{port}")
    print(f"Segment: judge_act3 -> {SEGMENT_ROUTES['judge_act3']['name']}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
