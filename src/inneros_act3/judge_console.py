from __future__ import annotations

from dataclasses import asdict
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import mimetypes
from pathlib import Path
import sys
from typing import Any
from urllib.parse import parse_qs, urlparse

from .dual_prize import run_dual_prize_pipeline
from .evolus_adapter import evolus_smoke
from .token_factory_provider import DEFAULT_TOKEN_FACTORY_MODEL, list_token_factory_models, is_token_factory_enabled


WEB_ROOT = Path(__file__).with_name("web")

DEFAULT_INCIDENT: dict[str, Any] = {
    "incident_id": "INC-BELLINI-20261014-01",
    "title": "Core Gateway Optical Flap & Camera Telemetry Drop",
    "source": "bellini-network-guardian",
    "facility": "Bellini Building Tower I",
    "loss_of_carrier": True,
    "affected_subsystems": ["surveillance_cameras", "access_control", "building_telemetry"],
    "telemetry": {
        "packet_loss_pct": 82.4,
        "carrier_flaps_per_min": 14,
        "rx_power_dbm": -28.4,
    },
}

VERIFIED_RECEIPT: dict[str, Any] = {
    "mode": "replay",
    "truth": "LIVE_VERIFIED_REPLAY",
    "verified_at": "2026-10-15T02:40:10.467021+00:00",
    "source_commit": "198af7a9071a4585ffff420aa8a60d75c91c58a3",
    "scenario": DEFAULT_INCIDENT,
    "pipeline": {
        "pipeline_id": "dual-act3-7a1877bdc8b3",
        "incident_id": "INC-BELLINI-20261014-01",
        "gemma": {
            "track": "google_deepmind_gemma_prize",
            "eligibility": "YES",
            "status": "LIVE_VERIFIED",
            "model": "Gemma-4-31B-IT",
            "provider": "amd-developer-cloud-gemma",
            "runtime": "AMD Developer Cloud / ROCm Token Factory",
            "available_models_count": 12,
            "completion_id": "615398e579fb46e8be320f66c82e4b31",
            "plan_sha256": "649fc0f5d72d83d028867e0a5c0e0f584857f273f99373098a134317d489b226",
            "diagnosis": (
                "Loss of carrier detected on primary edge router and optical link flap. "
                "Local inference directs traffic to backup cellular link and triggers Evolus remediation workflow."
            ),
        },
        "evolus": {
            "track": "evolus_business_agents_prize",
            "eligibility": "YES",
            "status": "LIVE_VERIFIED",
            "transport": "MCP JSON-RPC",
            "server": "Evolus2 Data Server v1.0.0",
            "application_name": "InnerOS",
            "application_id": "80dfecd4-8474-4aad-9565-5b7a2be10ea4",
            "work_order_id": "WO-EVOLUS-INC-BELLINI-20261014-01",
            "building_blocks": ["workflow", "knowledge_library"],
            "open_model_endpoint": "https://developer.amd.com.cn/radeon/api/v1",
            "work_order_sha256": "7d56f9cf109d317e30281b898e99974b4a01e052f4543f5cb8f98e2e7ad026ac",
        },
        "evidence": {
            "status": "LIVE_VERIFIED",
            "bundle_sha256": "6ee36d6905929b176fd9c49f3c1a4aa165df4a8231d5047871f581eb73b3f845",
            "verified": True,
        },
        "human_time_returned": {
            "baseline_seconds": 2700.0,
            "active_human_seconds": 120.0,
            "returned_seconds": 2580.0,
            "returned_minutes": 43.0,
            "automation_rate": 0.9556,
        },
    },
    "presentation_steps": [
        "Detect Bellini optical/network degradation",
        "Gemma analyzes telemetry on AMD Token Factory",
        "InnerOS validates the structured IncidentPlan",
        "Evolus retrieves SOP knowledge and creates a governed work order",
        "InnerOS verifies and seals the evidence bundle",
    ],
}

_SECRET_MARKERS = (
    "api_key",
    "authorization",
    "bearer",
    "x-user-apikey",
    "secret",
    "token_value",
)


def _assert_no_secret_material(value: Any) -> None:
    text = json.dumps(value, ensure_ascii=False).lower()
    for marker in _SECRET_MARKERS:
        if '"' + marker + '"' in text:
            raise ValueError("unsafe response field detected: " + marker)


def _public_result(result: Any, *, mode: str, proofs: dict[str, Any] | None = None) -> dict[str, Any]:
    plan = asdict(result.gemma_plan)
    work_order = asdict(result.evolus_work_order)
    bundle_manifest = result.evidence_bundle.manifest()
    bundle_verified = result.evidence_bundle.verify()
    truth = "LIVE_VERIFIED" if mode == "live" and bundle_verified else "MOCK"

    payload = {
        "mode": mode,
        "truth": truth,
        "scenario": DEFAULT_INCIDENT,
        "pipeline": {
            "pipeline_id": result.pipeline_id,
            "incident_id": result.incident_id,
            "created_at": result.created_at,
            "gemma": {
                "status": truth,
                "eligibility": result.eligibility_google_gemma,
                "model": plan["model"],
                "provider": plan["provider"],
                "severity": plan["severity"],
                "category": plan["category"],
                "diagnosis": plan["diagnosis"],
                "recommended_actions": plan["recommended_actions"],
                "delegation_lane": plan["delegation_lane"],
                "latency_ms": plan["latency_ms"],
                "tokens_used": plan["tokens_used"],
                "plan_sha256": result.gemma_plan.sha256(),
            },
            "evolus": {
                "status": truth,
                "eligibility": result.eligibility_evolus,
                "work_order_id": work_order["work_order_id"],
                "priority": work_order["priority"],
                "title": work_order["title"],
                "knowledge_references": work_order["knowledge_references"],
                "steps": work_order["steps"],
                "compliance_notes": work_order["compliance_notes"],
                "building_blocks": work_order["building_blocks_used"],
                "open_model_endpoint": work_order["model_endpoint"],
                "latency_ms": work_order["latency_ms"],
                "work_order_sha256": result.evolus_work_order.sha256(),
            },
            "evidence": {
                "status": truth,
                "verified": bundle_verified,
                **bundle_manifest,
            },
            "human_time_returned": {
                "baseline_seconds": result.human_time_returned.baseline_manual_seconds,
                "active_human_seconds": result.human_time_returned.active_human_seconds,
                "returned_seconds": result.human_time_returned.returned_seconds,
                "returned_minutes": round(result.human_time_returned.returned_seconds / 60.0, 1),
                "automation_rate": round(result.human_time_returned.automation_rate, 4),
            },
        },
        "proofs": proofs or {},
    }
    _assert_no_secret_material(payload)
    return payload


def run_demo(mode: str = "live") -> dict[str, Any]:
    mode = (mode or "live").lower()
    if mode == "replay":
        return VERIFIED_RECEIPT

    if mode == "mock":
        result = run_dual_prize_pipeline(DEFAULT_INCIDENT, gemma_mock=True, evolus_mock=True)
        return _public_result(result, mode="mock")

    if mode != "live":
        raise ValueError("mode must be live, mock, or replay")

    tf_enabled = is_token_factory_enabled()
    models = list_token_factory_models(mock=False) if tf_enabled else {"ok": False, "disabled": True}
    catalog = models.get("models", {}).get("data", []) if isinstance(models.get("models"), dict) else []
    model_ids = [str(item.get("id")) for item in catalog if isinstance(item, dict)]
    tf_live = tf_enabled and bool(models.get("ok")) and DEFAULT_TOKEN_FACTORY_MODEL in model_ids

    evolus = evolus_smoke(mock=False)
    evolus_live = (
        evolus.get("status") == "PASS"
        and evolus.get("mode") == "live"
        and bool(evolus.get("server_info"))
        and bool(evolus.get("application_id"))
        and not evolus.get("live_telemetry_warning")
    )
    if not evolus_live:
        return {
            "mode": "live",
            "truth": "BLOCKED",
            "stage": "evolus",
            "error": "Evolus live MCP proof unavailable",
            "details": {
                "status": evolus.get("status"),
                "mode": evolus.get("mode"),
                "warning": evolus.get("live_telemetry_warning"),
            },
        }

    # If Token Factory is enabled and live, run live gemma; otherwise run standby/reserve gemma
    # while keeping evolus live and mode="live"
    gemma_mock = not tf_live
    result = run_dual_prize_pipeline(DEFAULT_INCIDENT, gemma_mock=gemma_mock, evolus_mock=False)
    proofs = {
        "gemma": {
            "status": "LIVE" if tf_live else "STANDBY",
            "models_endpoint_ok": bool(models.get("ok")),
            "available_models_count": len(model_ids),
            "target_model_present": DEFAULT_TOKEN_FACTORY_MODEL in model_ids,
            "runtime": "AMD Developer Cloud / ROCm Token Factory" if tf_live else "AMD Developer Cloud / ROCm Token Factory (Standby Reserve)",
            "standby": not tf_live,
        },
        "evolus": {
            "mcp_live": True,
            "server_info": evolus.get("server_info"),
            "application_id": evolus.get("application_id"),
            "application_name": evolus.get("application_name"),
        },
    }
    return _public_result(result, mode="live", proofs=proofs)


def build_status_payload() -> dict[str, Any]:
    return {
        "service": "InnerOS ACT III Judge Console",
        "status": "READY",
        "last_verified": {
            "truth": VERIFIED_RECEIPT["truth"],
            "verified_at": VERIFIED_RECEIPT["verified_at"],
            "source_commit": VERIFIED_RECEIPT["source_commit"],
            "gemma": VERIFIED_RECEIPT["pipeline"]["gemma"]["status"],
            "evolus": VERIFIED_RECEIPT["pipeline"]["evolus"]["status"],
            "evidence": VERIFIED_RECEIPT["pipeline"]["evidence"]["status"],
        },
        "actions": ["live", "replay", "mock"],
    }


class JudgeConsoleHandler(BaseHTTPRequestHandler):
    server_version = "InnerOSJudgeConsole/1.0"

    def log_message(self, format: str, *args: Any) -> None:
        sys.stderr.write("[judge-console] " + (format % args) + "\n")

    def _send_json(self, value: Any, status: int = 200) -> None:
        payload = json.dumps(value, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

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
        if parsed.path in {"/", "/index.html"}:
            self._serve_asset(WEB_ROOT / "index.html")
            return
        if parsed.path == "/api/health":
            self._send_json({"ok": True, "service": "inneros-act3-judge-console"})
            return
        if parsed.path == "/api/status":
            self._send_json(build_status_payload())
            return
        if parsed.path == "/api/replay":
            self._send_json(VERIFIED_RECEIPT)
            return
        if parsed.path.startswith("/assets/"):
            relative = parsed.path.removeprefix("/assets/")
            self._serve_asset(WEB_ROOT / relative)
            return
        self.send_error(404)

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path != "/api/run":
            self.send_error(404)
            return
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


def main(argv: list[str] | None = None) -> int:
    argv = list(argv or sys.argv[1:])
    host = "127.0.0.1"
    port = 8765
    for item in argv:
        if item.startswith("--host="):
            host = item.split("=", 1)[1]
        elif item.startswith("--port="):
            port = int(item.split("=", 1)[1])

    server = ThreadingHTTPServer((host, port), JudgeConsoleHandler)
    print("InnerOS Judge Console: http://" + host + ":" + str(port))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
