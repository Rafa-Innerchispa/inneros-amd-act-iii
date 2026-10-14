# ACT III post-kickoff build lane

Baseline preserved at commit:
`458a22d284afb2c5cade4c5cb5872b6211eda609`

This branch contains only work performed after the hackathon kickoff boundary.

## Flagship demonstration

A real InnerOS workflow should prove, end to end:

1. human request enters the control plane;
2. capability and policy routing select the appropriate agent/skill;
3. local AMD ROCm execution is preferred;
4. fallback is explicit and evidence-backed;
5. tools/actions execute through bounded MCP/A2A lanes;
6. every task emits machine-readable execution evidence;
7. replay/verification can reconstruct what happened;
8. Human Time Returned quantifies business value.

## Demo workload

Primary narrative: autonomous operations for physical infrastructure / smart buildings.

Example:
- detect or receive an infrastructure incident;
- retrieve live telemetry and relevant knowledge;
- assign bounded specialist agents;
- execute an allowed remediation or produce a verified recommendation;
- show AMD execution metrics, decision reasons, evidence hash and time returned.

## Hackathon-only implementation targets

- live InnerOS coordination adapter
- AMD runtime probe
- task/skill execution manifest
- execution evidence export
- fallback visibility
- compact judge-facing timeline
- one repeatable real-world scenario

## Originality boundary

Pre-kickoff capabilities remain attributed to the baseline.
Only code and integrations added on this branch after kickoff are described as ACT III build-window work.
