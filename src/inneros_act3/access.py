from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
import secrets
import time
from dataclasses import dataclass
from typing import Any

SESSION_COOKIE = "inneros_access_session"
DEFAULT_SESSION_TTL = 8 * 60 * 60  # 8 hours
PBKDF2_ITERATIONS = 260_000

# Verified PBKDF2-HMAC-SHA256 hash of the initial judge runtime credential
# NEVER store plaintext credentials in code or repository.
DEFAULT_JUDGE_USER = "amd-judge"
DEFAULT_JUDGE_HASH = "pbkdf2_sha256$260000$TCYugF0_xdC8SPevKVIAPw$kAevyumgoKHDHxQ1Jefsaudkjj4rSdJ2lP7QX0z9i-o"

SEGMENT_ROUTES: dict[str, dict[str, Any]] = {
    "judge_act3": {
        "name": "AMD ACT III Judge Console",
        "segment": "judge_act3",
        "default_path": "/",
        "allowed_roles": ["judge_act3", "owner", "admin"],
    },
    # Future segments: voiceops, bellini, energy, admin
}


def _b64e(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _b64d(value: str) -> bytes:
    return base64.urlsafe_b64decode(value + "=" * (-len(value) % 4))


def hash_password(password: str, *, salt: bytes | None = None, iterations: int = PBKDF2_ITERATIONS) -> str:
    if len(password) < 8:
        raise ValueError("password must be at least 8 characters")
    salt = salt or secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)
    return f"pbkdf2_sha256${iterations}${_b64e(salt)}${_b64e(digest)}"


def verify_password(password: str, encoded: str) -> bool:
    try:
        scheme, iterations_raw, salt_raw, digest_raw = encoded.split("$", 3)
        if scheme != "pbkdf2_sha256":
            return False
        iterations = int(iterations_raw)
        salt = _b64d(salt_raw)
        expected = _b64d(digest_raw)
    except (TypeError, ValueError):
        return False
    actual = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)
    return hmac.compare_digest(actual, expected)


@dataclass(frozen=True)
class AuthPrincipal:
    subject: str
    username: str
    role: str
    segment: str
    display_name: str
    auth_source: str
    issued_at: int
    expires_at: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "subject": self.subject,
            "username": self.username,
            "role": self.role,
            "segment": self.segment,
            "display_name": self.display_name,
            "auth_source": self.auth_source,
            "issued_at": self.issued_at,
            "expires_at": self.expires_at,
        }


class RateLimiter:
    def __init__(self, max_attempts: int = 5, window_seconds: int = 60) -> None:
        self.max_attempts = max_attempts
        self.window_seconds = window_seconds
        self._attempts: dict[str, list[float]] = {}

    def is_rate_limited(self, key: str) -> bool:
        now = time.time()
        cutoff = now - self.window_seconds
        history = [ts for ts in self._attempts.get(key, []) if ts > cutoff]
        self._attempts[key] = history
        return len(history) >= self.max_attempts

    def record_failure(self, key: str) -> None:
        now = time.time()
        cutoff = now - self.window_seconds
        history = [ts for ts in self._attempts.get(key, []) if ts > cutoff]
        history.append(now)
        self._attempts[key] = history

    def reset(self, key: str) -> None:
        self._attempts.pop(key, None)


class AccessManager:
    def __init__(
        self,
        *,
        session_secret: str | None = None,
        judge_user: str | None = None,
        judge_password_hash: str | None = None,
        session_ttl_seconds: int = DEFAULT_SESSION_TTL,
        rate_limiter: RateLimiter | None = None,
    ) -> None:
        secret_value = session_secret or os.getenv("INNEROS_ACCESS_SECRET") or secrets.token_urlsafe(48)
        self.session_secret = secret_value.encode("utf-8")
        self.judge_user = (judge_user or os.getenv("INNEROS_ACCESS_JUDGE_USER") or DEFAULT_JUDGE_USER).strip()
        self.judge_password_hash = (
            judge_password_hash
            or os.getenv("INNEROS_ACCESS_JUDGE_HASH")
            or DEFAULT_JUDGE_HASH
        ).strip()
        self.session_ttl_seconds = max(300, int(session_ttl_seconds))
        self.rate_limiter = rate_limiter or RateLimiter()

    def _sign(self, payload: dict[str, Any]) -> str:
        raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        body = _b64e(raw)
        sig = _b64e(hmac.new(self.session_secret, body.encode("ascii"), hashlib.sha256).digest())
        return f"{body}.{sig}"

    def _verify(self, token: str) -> dict[str, Any] | None:
        if not token or "." not in token:
            return None
        try:
            body, sig = token.rsplit(".", 1)
            expected = _b64e(hmac.new(self.session_secret, body.encode("ascii"), hashlib.sha256).digest())
            if not hmac.compare_digest(sig, expected):
                return None
            payload = json.loads(_b64d(body).decode("utf-8"))
            if not isinstance(payload, dict):
                return None
            if int(payload.get("exp") or 0) <= int(time.time()):
                return None
            return payload
        except Exception:
            return None

    def issue_session(self, principal: AuthPrincipal) -> str:
        payload = {
            "kind": "access_session",
            "sub": principal.subject,
            "usr": principal.username,
            "role": principal.role,
            "seg": principal.segment,
            "name": principal.display_name,
            "src": principal.auth_source,
            "iat": principal.issued_at,
            "exp": principal.expires_at,
        }
        return self._sign(payload)

    def verify_session_token(self, token: str) -> AuthPrincipal | None:
        payload = self._verify(token)
        if not payload or payload.get("kind") != "access_session":
            return None
        role = str(payload.get("role") or "")
        segment = str(payload.get("seg") or "judge_act3")
        return AuthPrincipal(
            subject=str(payload.get("sub") or ""),
            username=str(payload.get("usr") or ""),
            role=role,
            segment=segment,
            display_name=str(payload.get("name") or "InnerOS Evaluator"),
            auth_source=str(payload.get("src") or "unknown"),
            issued_at=int(payload.get("iat") or 0),
            expires_at=int(payload.get("exp") or 0),
        )

    def extract_session_token(self, cookie_header: str | None) -> str | None:
        if not cookie_header:
            return None
        cookies = [c.strip() for c in cookie_header.split(";")]
        for item in cookies:
            if "=" in item:
                k, v = item.split("=", 1)
                if k.strip() == SESSION_COOKIE:
                    return v.strip()
        return None

    def authenticate(self, username: str, password: str, *, client_ip: str = "") -> tuple[AuthPrincipal | None, str | None]:
        rate_key = client_ip or username.strip()
        if self.rate_limiter.is_rate_limited(rate_key):
            return None, "rate_limited"

        clean_user = username.strip()
        if not clean_user or not password:
            self.rate_limiter.record_failure(rate_key)
            return None, "invalid_credentials"

        if not hmac.compare_digest(clean_user, self.judge_user) or not verify_password(password, self.judge_password_hash):
            self.rate_limiter.record_failure(rate_key)
            return None, "invalid_credentials"

        self.rate_limiter.reset(rate_key)
        now = int(time.time())
        principal = AuthPrincipal(
            subject=f"judge:{clean_user}",
            username=clean_user,
            role="judge_act3",
            segment="judge_act3",
            display_name="AMD ACT III Judge",
            auth_source="judge_credentials",
            issued_at=now,
            expires_at=now + self.session_ttl_seconds,
        )
        return principal, None
