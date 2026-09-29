from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import hashlib
import json
from typing import Literal

TruthState = Literal["PROVEN", "PARTIAL", "CONTRACT-ONLY", "PLANNED"]


def _canonical(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


@dataclass(frozen=True)
class RuntimeIdentity:
    target: str
    provider: str
    accelerator: str
    architecture: str
    runtime: str
    model: str
    truth_state: TruthState = "PROVEN"


@dataclass(frozen=True)
class HumanTimeReturned:
    baseline_manual_seconds: float
    active_human_seconds: float
    source: Literal["MEASURED", "ESTIMATED"] = "MEASURED"

    @property
    def returned_seconds(self) -> float:
        return max(0.0, self.baseline_manual_seconds - self.active_human_seconds)

    @property
    def automation_rate(self) -> float:
        if self.baseline_manual_seconds <= 0:
            return 0.0
        return max(0.0, min(1.0, self.returned_seconds / self.baseline_manual_seconds))


@dataclass(frozen=True)
class ExecutionEvidence:
    run_id: str
    task_id: str
    route_target: str
    route_reasons: tuple[str, ...]
    runtime: RuntimeIdentity
    started_at: str
    elapsed_ms: float
    success: bool
    output_sha256: str
    human_time: HumanTimeReturned | None = None

    def canonical_json(self) -> str:
        return _canonical(asdict(self))

    def sha256(self) -> str:
        return hashlib.sha256(self.canonical_json().encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class EvidenceBundle:
    schema: str
    created_at: str
    executions: tuple[ExecutionEvidence, ...]

    @classmethod
    def create(cls, executions: tuple[ExecutionEvidence, ...]) -> "EvidenceBundle":
        return cls(
            schema="inneros.act3.evidence.v1",
            created_at=datetime.now(timezone.utc).isoformat(),
            executions=executions,
        )

    def manifest(self) -> dict[str, object]:
        execution_hashes = [item.sha256() for item in self.executions]
        body = {
            "schema": self.schema,
            "created_at": self.created_at,
            "execution_hashes": execution_hashes,
        }
        body["bundle_sha256"] = hashlib.sha256(
            _canonical(body).encode("utf-8")
        ).hexdigest()
        return body

    def verify(self) -> bool:
        manifest = self.manifest()
        expected = manifest["bundle_sha256"]
        body = {
            "schema": manifest["schema"],
            "created_at": manifest["created_at"],
            "execution_hashes": manifest["execution_hashes"],
        }
        actual = hashlib.sha256(_canonical(body).encode("utf-8")).hexdigest()
        return actual == expected


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()
