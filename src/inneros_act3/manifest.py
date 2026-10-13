from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Iterable


@dataclass(frozen=True)
class Capability:
    name: str
    kind: str
    runtime: str
    local_first: bool = True
    evidence_required: bool = True


DEFAULT_CAPABILITIES = (
    Capability("local_inference", "model", "amd_rocm"),
    Capability("skills", "orchestration", "inneros"),
    Capability("mcp_tools", "tooling", "mcp"),
    Capability("a2a_agents", "orchestration", "a2a"),
    Capability("durable_workflows", "coordination", "temporal"),
    Capability("execution_evidence", "audit", "inneros"),
)


def capability_manifest(capabilities: Iterable[Capability] = DEFAULT_CAPABILITIES) -> dict:
    items = [asdict(item) for item in capabilities]
    return {
        "schema": "inneros.act3.capability-manifest.v1",
        "local_first": True,
        "capabilities": items,
    }
