# ACT III Canonical State — 2026-10-14

This document is the current continuity source for the ACT III implementation. It exists so the project does not depend on any single chat session.

## Product direction

InnerOS is evolving from a multi-agent coordination layer into a local-first operating fabric that connects:

- human interfaces such as VoiceOps and WhatsApp owner control;
- local AMD/Intel compute;
- cloud specialist models;
- persistent/shared memory;
- domain agents;
- physical infrastructure;
- business workflows;
- human approval;
- execution evidence and replay.

The ACT III demo should prove the fabric as one continuous workflow, not as a list of integrations.

## Core demo story

The flagship flow remains a Bellini smart-building incident:

1. An operator asks by VoiceOps what happened to cameras/intercom/building services.
2. InnerOS creates the incident context.
3. AG-60 / Bellini / Device Fabric / Guardian contribute topology, telemetry and asset evidence.
4. Cognee contributes curated prior shared memory when relevant.
5. Gemma-4-31B-IT on AMD Token Factory acts as the **Multimodal Incident Director**.
6. Gemma returns a schema-validated `IncidentPlan` containing:
   - incident_summary
   - hypotheses[]
   - evidence_refs[]
   - contradictions[]
   - required_tools[]
   - delegated_tasks[]
   - risk_level
   - approval_required
   - next_best_action
7. InnerOS converts the plan into governed MCP/A2A work.
8. Local AMD/Intel agents execute first.
9. Consequential actions stop for owner approval.
10. Results are verified.
11. Evolus can transform the verified technical result into a business workflow/work order.
12. InnerOS seals provider/model/agent/tool/approval/verification evidence for replay.

## AMD Token Factory / Google DeepMind Gemma

Owner evidence on 2026-10-14 confirms:

- Token Factory account active
- team: `team-428`
- team size: 1
- redemption complete
- active shared API credential available
- `Gemma-4-31B-IT` visible in the current model catalog

The credential itself must not be written into Git. It has been delivered to the Antigravity execution lane with instructions to persist it through the existing InnerOS Owner Vault and use only the resulting vault reference/runtime environment.

Canonical runtime values:

```text
provider = AMD Token Factory
base_url = https://developer.amd.com.cn/radeon/api/v1
model = Gemma-4-31B-IT
credential_ref = owner_vault:amd_token_factory/api_key
```

Official AMD Radeon Cloud docs describe the public shared endpoints as OpenAI-compatible, always on and free for development/hackathon use. The current model must still be resolved through `GET /models` at runtime because the catalog can change.

### Required live proof

Antigravity must produce:

- successful `GET /models`;
- current presence of `Gemma-4-31B-IT`;
- successful `POST /chat/completions`;
- structured IncidentPlan validation;
- provider/model/base-url evidence without exposing credentials;
- latency/token metadata when returned;
- repo commit/tests.

Task/correlation:

`ops_b4c988b85337`
`act3-gemma-evolus-20261014`

## Cognee shared memory

Cognee is an InnerOS capability, not an ACT III prize partner.

Existing implementation already lives in:

`Rafa-Innerchispa/inneros-personal-brain`

Key reusable pieces:

- `app/cognee_agent_tools.py`
- `app/cognee_mcp_proxy.py`
- `app/memory_fabric.py`
- `docs/COGNEE_AGENT_MEMORY_FABRIC.md`
- `docs/VOICEOPS_SHARED_MEMORY_BRIDGE.md`

ACT III proof:

`Agent A learns -> curated safe memory -> Cognee -> Agent B remembers`

Private customer/secrets/operational payloads remain in private InnerOS memory; only curated facts/decisions/outcomes enter shared memory.

Current task:

`ops_4ccf470eff0e`
`act3-cognee-memory-20261014`

## Evolus

Evolus is an optional ACT III business-agent partner lane.

Owner has created/logged into an Evolus account, but as of the current state the visible account still appears to be a normal trial with zero event credits. The event workspace/code still needs to be resolved before claiming the hackathon 50,000-credit allocation.

Target architecture:

```text
verified InnerOS incident
  -> Evolus Workflow
  -> Evolus Knowledge Library
  -> structured work order / escalation
  -> return to InnerOS
  -> approval / evidence / replay
```

Minimum building blocks:
- Workflow
- Knowledge Library

Important truth boundary:
The shared AMD Token Factory endpoint is sufficient for the Google/Gemma proof once live-tested. Evolus may require a dedicated self-hosted vLLM endpoint on AMD Developer Cloud. Do not claim the shared endpoint satisfies that requirement unless the official track validation accepts it.

## Gemini 4 Argon

Argon is an InnerOS advanced specialist, not the ACT III Gemma partner requirement.

Role:
- large-codebase reasoning
- difficult software engineering
- architecture
- long-horizon debugging
- red-team/final review
- high-complexity agent tasks

It must remain behind local-first routing and a hard application-side cost governor.

Default owner policy:

```text
monthly hard budget = USD 10
daily budget = USD 2
default per-call estimated maximum = USD 0.75
concurrency = 1
default thinking = medium
high thinking = explicit hard/P0 only
default context ceiling = 150k tokens
default max output = 32768
```

Required mechanisms:
- preflight token count
- cost reservation before call
- durable spend ledger
- postflight actual usage reconciliation
- fail closed on budget violation
- owner-readable spend status
- native Google spend cap/alerts as a second layer where supported

Current task:

`ops_945efe8662c0`
`inneros-gemini-4-argon-cost-20261014`

## Current model hierarchy

```text
InnerOS
  |
  +-- Local AMD R9700 / ROCm / Qwen
  |     default private operational reasoning
  |
  +-- AMD Token Factory / Gemma-4-31B-IT
  |     ACT III Multimodal Incident Director
  |
  +-- Cognee
  |     curated cross-agent shared memory
  |
  +-- Evolus
  |     business workflow / work-order specialist
  |
  +-- Gemini 4 Argon
        governed deep-engineering specialist with cost cap
```

Product principle:

**InnerOS does not choose the most powerful model. It chooses the right intelligence, at the right cost, under the right authority.**

## Presentation / video status

Do not finalize the visual deck until:
- live Gemma Token Factory proof exists;
- Cognee memory proof is captured;
- Evolus event workspace eligibility is resolved;
- Argon provider/cost governor status is known.

The final deck should show real evidence/screenshots for these flows rather than logos-only partner slides.

## Canonical related documents

- `docs/INNEROS_INTEGRATION_MAP.md`
- `docs/GEMMA_ARGON_STRATEGY.md`
- `docs/BELLINI_CASE_STUDY.md`
- `docs/PARTNER_GOOGLE_EVOLUS_PLAN.md`
- `submission/NARRATIVE.md`
- `submission/VIDEO_SCRIPT.md`
- `submission/SLIDE_DECK_OUTLINE.md`

## Truth rule

Only capabilities with live/captured evidence may be presented as LIVE. Code-ready, configured, simulated and planned states must remain clearly distinguished.
