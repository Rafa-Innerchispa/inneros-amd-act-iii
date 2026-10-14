# Antigravity Task — ACT III Google Live Proof

Status: **READY TO EXECUTE WHEN INNEROS MCP RECOVERS**

## Purpose

Turn the existing InnerOS Google integration from “implemented/configured components” into one small, captured, judge-safe LIVE path for ACT III.

Do not redesign InnerOS and do not make Google the main orchestrator.

## Existing components

- `platform/inneros_core_runtime/gemini_runtime.py`
  - Gemini / Vertex provider
  - governed tools
  - Firestore evidence
  - Pub/Sub events
  - Model Armor path
- `platform/inneros_core_runtime/gcp_memory_bank.py`
  - Firestore agent-memory mirror
- `platform/inneros_core_runtime/google_adk_a2a.py`
  - Google ADK / RemoteA2aAgent contract
  - currently truth-labeled NON-LIVE / quota-blocked where appropriate
- `platform/inneros_core_runtime/agents/ag44_cloud_deployer.py`
  - GCP auth/readiness
  - project/billing inspection
  - dry-run planning
  - owner approval gates

Metadata refresh PR:
`Rafa-Innerchispa/innerops-agentic-platform#181`

## Required live proof

Safest useful target:

`InnerOS ACT III Bellini correlation -> sanitized evidence/event -> Firestore and/or Pub/Sub -> captured receipt`

Optional only if quota/provider access works:

`sanitized incident summary -> Gemini/Vertex bounded specialist review -> response returned to InnerOS evidence`

## Requirements

1. No production Bellini mutation.
2. No plaintext credentials in logs/Git/chat.
3. Use server-side existing Google auth only.
4. Preserve correlation ID from InnerOS.
5. Capture provider/runtime identity and timestamps.
6. Keep local AMD reasoning as the main demo path.
7. Do not change any NON-LIVE label to LIVE without actual same-run evidence.
8. If Gemini quota is blocked, Firestore/PubSub live evidence is still valuable; report Gemini blocker truthfully.
9. Add sanitized ACT III evidence file or runbook only in the appropriate hackathon/evidence location.
10. Do not enable broad cloud mutations.

## Deliverables

- AG-44 provider status
- GCP authorization readiness (sanitized)
- Firestore/PubSub live result PASS/FAIL
- Gemini/Vertex bounded review PASS/FAIL/BLOCKED
- correlation ID
- evidence path
- any safe fixes on isolated branch
- exact remaining human/account action if blocked

## Definition of done

ACT III can truthfully say either:

A) **Google live path demonstrated** with captured evidence, or

B) **Google integration implemented but live partner proof blocked by quota/account condition**, with exact evidence and no false claim.
