from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from typing import Literal

from .core import RouteRequest, route
from .evidence import (
    EvidenceBundle,
    ExecutionEvidence,
    HumanTimeReturned,
    RuntimeIdentity,
    sha256_text,
)

ScenarioState = Literal["CONTRACT-ONLY", "LIVE-PARTIAL", "PROVEN"]


@dataclass(frozen=True)
class ScenarioStep:
    step_id: str
    agent: str
    skill: str
    action: str
    mutating: bool
    requires_human_approval: bool
    route_request: RouteRequest
    synthetic_output: str
    manual_baseline_seconds: float
    active_human_seconds: float


@dataclass(frozen=True)
class ScenarioStepReceipt:
    step_id: str
    agent: str
    skill: str
    action: str
    mutating: bool
    requires_human_approval: bool
    route_target: str
    route_reasons: tuple[str, ...]
    execution_sha256: str


@dataclass(frozen=True)
class ScenarioResult:
    schema: str
    scenario_id: str
    title: str
    state: ScenarioState
    receipts: tuple[ScenarioStepReceipt, ...]
    evidence_manifest: dict[str, object]
    total_human_time_returned_seconds: float
    all_mutations_guarded: bool

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


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
        accelerator="TBA",
        architecture="TBA",
        runtime="ROCm",
        model="TBA",
        truth_state="CONTRACT-ONLY",
    )


def smart_building_incident_steps() -> tuple[ScenarioStep, ...]:
    return (
        ScenarioStep(
            step_id="incident-intake",
            agent="ops-intake",
            skill="incident_triage",
            action="Normalize a report that cameras and intercom video are intermittently unavailable.",
            mutating=False,
            requires_human_approval=False,
            route_request=RouteRequest(privacy_required=True, latency_sensitive=True),
            synthetic_output="incident=video-degradation scope=building-network severity=medium",
            manual_baseline_seconds=180.0,
            active_human_seconds=20.0,
        ),
        ScenarioStep(
            step_id="telemetry-correlation",
            agent="network-guardian",
            skill="telemetry_correlation",
            action="Correlate link, reachability and device-health evidence.",
            mutating=False,
            requires_human_approval=False,
            route_request=RouteRequest(privacy_required=True, latency_sensitive=True),
            synthetic_output="evidence=link-loss+camera-gaps suspected-path=backbone",
            manual_baseline_seconds=600.0,
            active_human_seconds=45.0,
        ),
        ScenarioStep(
            step_id="knowledge-retrieval",
            agent="knowledge-agent",
            skill="grounded_retrieval",
            action="Retrieve topology, prior incidents and vendor constraints.",
            mutating=False,
            requires_human_approval=False,
            route_request=RouteRequest(privacy_required=True),
            synthetic_output="topology=matched prior_incident=found constraints=read-only-first",
            manual_baseline_seconds=480.0,
            active_human_seconds=30.0,
        ),
        ScenarioStep(
            step_id="remediation-plan",
            agent="repair-planner",
            skill="bounded_remediation_plan",
            action="Produce the lowest-risk remediation plan and rollback.",
            mutating=False,
            requires_human_approval=False,
            route_request=RouteRequest(latency_sensitive=True),
            synthetic_output="plan=reroute-or-port-remediation rollback=preserve-current-path",
            manual_baseline_seconds=420.0,
            active_human_seconds=35.0,
        ),
        ScenarioStep(
            step_id="authorized-action",
            agent="ops-executor",
            skill="approved_network_action",
            action="Execute a bounded remediation only after explicit approval.",
            mutating=True,
            requires_human_approval=True,
            route_request=RouteRequest(privacy_required=True, latency_sensitive=True),
            synthetic_output="action=bounded-remediation approval=required rollback=ready",
            manual_baseline_seconds=300.0,
            active_human_seconds=60.0,
        ),
        ScenarioStep(
            step_id="verification",
            agent="evidence-verifier",
            skill="forensic_replay",
            action="Verify outcome and emit replayable evidence.",
            mutating=False,
            requires_human_approval=False,
            route_request=RouteRequest(privacy_required=True),
            synthetic_output="verification=pass replay=available evidence=sealed",
            manual_baseline_seconds=240.0,
            active_human_seconds=20.0,
        ),
    )


def run_scenario(
    steps: tuple[ScenarioStep, ...] | None = None,
    *,
    state: ScenarioState = "CONTRACT-ONLY",
) -> ScenarioResult:
    scenario_steps = steps or smart_building_incident_steps()
    executions: list[ExecutionEvidence] = []
    receipts: list[ScenarioStepReceipt] = []

    for index, step in enumerate(scenario_steps, start=1):
        routing = route(step.route_request)
        output = {
            "step_id": step.step_id,
            "agent": step.agent,
            "skill": step.skill,
            "action": step.action,
            "result": step.synthetic_output,
            "route_target": routing.target,
            "route_reasons": routing.reason_codes,
        }
        execution = ExecutionEvidence(
            run_id=f"act3-smart-building-{index:02d}",
            task_id=step.step_id,
            route_target=routing.target,
            route_reasons=routing.reason_codes,
            runtime=_runtime_for(routing.target),
            started_at=f"2026-10-13T10:00:{index:02d}+00:00",
            elapsed_ms=float(index * 175),
            success=True,
            output_sha256=sha256_text(json.dumps(output, sort_keys=True)),
            human_time=HumanTimeReturned(
                baseline_manual_seconds=step.manual_baseline_seconds,
                active_human_seconds=step.active_human_seconds,
                source="ESTIMATED",
            ),
        )
        executions.append(execution)
        receipts.append(
            ScenarioStepReceipt(
                step_id=step.step_id,
                agent=step.agent,
                skill=step.skill,
                action=step.action,
                mutating=step.mutating,
                requires_human_approval=step.requires_human_approval,
                route_target=routing.target,
                route_reasons=routing.reason_codes,
                execution_sha256=execution.sha256(),
            )
        )

    bundle = EvidenceBundle(
        schema="inneros.act3.evidence.v1",
        created_at="2026-10-13T10:01:00+00:00",
        executions=tuple(executions),
    )
    total_returned = sum(
        execution.human_time.returned_seconds
        for execution in executions
        if execution.human_time is not None
    )
    all_mutations_guarded = all(
        (not receipt.mutating) or receipt.requires_human_approval
        for receipt in receipts
    )
    return ScenarioResult(
        schema="inneros.act3.scenario.v1",
        scenario_id="smart-building-network-incident",
        title="Autonomous smart-building incident response",
        state=state,
        receipts=tuple(receipts),
        evidence_manifest=bundle.manifest(),
        total_human_time_returned_seconds=total_returned,
        all_mutations_guarded=all_mutations_guarded,
    )


def main() -> None:
    result = run_scenario()
    print(json.dumps(result.as_dict(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
