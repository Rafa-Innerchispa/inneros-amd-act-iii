# Antigravity Task — ACT III Evolus Partner Integration

Status: **READY TO EXECUTE WHEN MCP/AGENT BINDING RECOVERS**

Reason for durable file: the InnerOS compact MCP currently returns upstream 502 errors, so the task could not be reliably dispatched through coordination at the time this file was created.

## Mission

Build the smallest credible Evolus partner integration for ACT III **without changing the core InnerOS architecture and without touching production services**.

Repository:
`Rafa-Innerchispa/inneros-amd-act-iii`

Base:
`hackathon/act3-build-20261013`

Work branch:
`antigravity/act3-evolus-partner-20261014`

## Architecture

`InnerOS Bellini incident -> Evolus Workflow -> Evolus Knowledge Library -> structured business result -> InnerOS approval/evidence`

InnerOS remains:
- orchestrator/control plane;
- owner of human approval;
- owner of physical/network actions;
- owner of audit evidence.

Evolus is a bounded business-process specialist.

## Model placement

Do **not** load another model on the local Radeon AI PRO R9700.

Use a separate open instruct model through vLLM on AMD Developer Cloud / Token Factory as required by the Evolus ACT III partner track.

## Required Evolus building blocks

Minimum two:
1. Workflow
2. Knowledge Library

Optional third:
- MCP connector

## Bellini workflow

Input from InnerOS:
- sanitized incident ID
- sanitized failure-domain summary
- affected service classes
- evidence labels
- recommended follow-up type

Evolus should:
1. receive the incident through API;
2. query sanitized runbooks/knowledge;
3. classify operational/business impact;
4. produce a structured work-order/escalation draft;
5. return JSON to InnerOS;
6. never execute building/network changes directly.

## Code tasks

1. Add Evolus adapter under ACT III repo.
2. Configuration only via environment variables.
3. No secrets in Git/logs/tests.
4. Add mock/dry-run tests.
5. Add one live smoke-test command gated on env credentials.
6. Add `docs/EVOLUS_PARTNER.md` with setup and truth boundaries.
7. Preserve correlation ID between InnerOS and Evolus.
8. Record request/result evidence without API key.
9. Container path must remain compatible with ACT III public demo.

## Manual prerequisites from Rafael

The task may proceed through mock implementation immediately, but live eligibility requires:

- Evolus ACT III event workspace
- event code from kickoff
- Evolus API key stored server-side
- AMD Developer Cloud/Token Factory access
- public/private vLLM endpoint reachable by Evolus as required by the event

If these are missing, stop only the LIVE portion and report the exact account/auth blocker. Do not stop code/docs/tests.

## Safety

Do not modify:
- production InnerOS runtime
- VoiceOps/PBX
- local R9700 model services
- MC2/MC3/MC4
- Bellini network/device configuration

No paid APIs. Use event credits/free resources only.

## Definition of done

- branch pushed
- adapter implemented
- tests green
- Workflow + Knowledge Library design documented
- env-variable contract documented
- AMD cloud vLLM config documented
- live smoke PASS if prerequisites exist, otherwise exact blocker
- no secret leakage
- result ready to connect to main ACT III demo without redesign
