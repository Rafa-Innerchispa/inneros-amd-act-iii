from __future__ import annotations

from dataclasses import asdict
import json

from .core import RouteRequest, route, verify_evidence
from .evidence import (
    EvidenceBundle,
    ExecutionEvidence,
    HumanTimeReturned,
    RuntimeIdentity,
    sha256_text,
)


def _runtime_for(target: str) -> RuntimeIdentity:
    if target == "amd-local":
        return RuntimeIdentity(
            target="amd-local",
            provider="InnerOS local",
            accelerator="AMD Radeon AI PRO R9700",
            architecture="gfx1201",
            runtime="ROCm",
            model="Qwen local",
            truth_state="PROVEN",
        )
    return RuntimeIdentity(
        target="amd-cloud",
        provider="AMD cloud",
        accelerator="TBA at ACT III kickoff",
        architecture="TBA",
        runtime="ROCm",
        model="TBA",
        truth_state="CONTRACT-ONLY",
    )


def build_demo_bundle() -> EvidenceBundle:
    samples = [
        ("private-workload", RouteRequest(privacy_required=True), 600.0, 45.0),
        ("elastic-workload", RouteRequest(needs_elastic_capacity=True), 900.0, 90.0),
        ("local-fast-path", RouteRequest(latency_sensitive=True), 300.0, 30.0),
        ("local-unavailable", RouteRequest(local_available=False), 420.0, 60.0),
    ]
    executions: list[ExecutionEvidence] = []

    for index, (name, request, manual_s, human_s) in enumerate(samples, start=1):
        routing = route(request)
        routing_digest = routing.sha256()
        assert verify_evidence(routing, routing_digest)
        synthetic_output = json.dumps(
            {
                "workload": name,
                "target": routing.target,
                "reasons": routing.reason_codes,
            },
            sort_keys=True,
        )
        executions.append(
            ExecutionEvidence(
                run_id=f"demo-run-{index}",
                task_id=name,
                route_target=routing.target,
                route_reasons=routing.reason_codes,
                runtime=_runtime_for(routing.target),
                started_at=f"2026-09-28T00:00:0{index}+00:00",
                elapsed_ms=float(index * 250),
                success=True,
                output_sha256=sha256_text(synthetic_output),
                human_time=HumanTimeReturned(
                    baseline_manual_seconds=manual_s,
                    active_human_seconds=human_s,
                    source="ESTIMATED",
                ),
            )
        )
    return EvidenceBundle(
        schema="inneros.act3.evidence.v1",
        created_at="2026-09-28T00:00:10+00:00",
        executions=tuple(executions),
    )


def main() -> None:
    bundle = build_demo_bundle()
    manifest = bundle.manifest()
    payload = {
        "manifest": manifest,
        "verified": bundle.verify(),
        "executions": [asdict(item) for item in bundle.executions],
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
