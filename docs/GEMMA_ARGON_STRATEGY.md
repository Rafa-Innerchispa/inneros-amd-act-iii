# ACT III — Gemma + Argon Strategy

## Why this exists

InnerOS uses multiple models for different jobs. ACT III should make that visible without turning the demo into a model zoo.

The product rule is:

**local first, specialist cloud only when the workload justifies it, and every paid/cloud route remains governed and evidenced.**

## Gemma in ACT III: Multimodal Incident Director

Gemma is not a decorative second opinion.

The ACT III Google/AMD proof should make `Gemma-4-31B-IT`, served through AMD Token Factory, an essential visible step in the Bellini incident workflow.

### Input

InnerOS gathers heterogeneous evidence:

- VoiceOps transcript / operator intent
- Bellini topology, dashboard or incident image
- AG-60 / Device Fabric telemetry
- curated prior memory from Cognee when available
- relevant current incident facts

### Gemma output

Gemma returns a schema-checked `IncidentPlan`:

- `incident_summary`
- `hypotheses[]`
- `evidence_refs[]`
- `contradictions[]`
- `required_tools[]`
- `delegated_tasks[]`
- `risk_level`
- `approval_required`
- `next_best_action`

Gemma never mutates infrastructure directly. InnerOS translates the plan into governed MCP/A2A work.

### Execution

1. VoiceOps receives the operator question.
2. InnerOS creates the incident context.
3. AG-60 / Guardian / Device Fabric provide physical-world evidence.
4. Cognee recalls safe relevant prior knowledge.
5. Gemma-4-31B-IT on AMD Token Factory fuses multimodal evidence and produces the incident plan.
6. InnerOS delegates bounded work to local agents.
7. Local AMD/Intel agents execute probes first.
8. Results return to InnerOS; an optional second Gemma pass reconciles conflicting evidence.
9. Evolus converts the verified incident into the business workflow / work order using Workflow + Knowledge Library.
10. InnerOS retains approval, action, verification and evidence/replay.

### Evidence shown to judges

- provider: AMD Token Factory
- model: Gemma-4-31B-IT
- role: multimodal_incident_director
- input modalities
- evidence references
- agents/tools delegated
- latency / token usage when returned
- AMD route proof
- final verification and Human Time Returned

## Why this is different from current ACT III submissions

Several public ACT III entries already perform useful single-model industrial diagnosis:
- image + sensor + manual -> diagnosis/work order;
- document RAG;
- visual defect inspection.

InnerOS differentiates by demonstrating a persistent operating fabric:

**voice + multimodal evidence + live/captured physical infrastructure + shared memory + multi-agent delegation + human approval + business workflow + replayable evidence.**

Gemma does not replace InnerOS. It becomes one powerful reasoning node inside it.

## Gemini 4 Argon in InnerOS

Argon is a separate InnerOS capability, not the Google partner requirement for ACT III.

Role:
- complex software engineering;
- large-codebase reasoning;
- architecture review;
- hard debugging;
- red-team / final review;
- long-horizon agent tasks.

It should not handle routine VoiceOps or inexpensive everyday requests.

### Cost policy

InnerOS must enforce a hard application-side budget before Argon is generally enabled:

- monthly hard budget: USD 10
- daily budget: USD 2
- default per-call estimated maximum: USD 0.75
- concurrency: 1
- default thinking: medium
- high thinking only for explicit hard/P0 routing
- default context ceiling: 150k tokens
- default max output: 32768
- preflight token count
- durable reservation and cost ledger
- postflight usage reconciliation

Current official pricing:
- through 2026-11-30: USD 2 / 1M input; USD 10 / 1M output
- from 2026-12-01: USD 4 / 1M input; USD 20 / 1M output
- implicit cached input receives a 95% discount
- thinking tokens are billed as output

Argon should appear in the ACT III presentation as evidence that InnerOS can route advanced workloads to a governed frontier specialist, while the actual Google partner demo remains Gemma running on AMD.

## Model hierarchy for the pitch

```text
InnerOS
  |
  +-- Local AMD R9700 / ROCm / Qwen
  |     default private operational reasoning
  |
  +-- AMD Token Factory / Gemma-4-31B-IT
  |     ACT III multimodal incident director
  |
  +-- Gemini 4 Argon
  |     governed deep-engineering / long-horizon specialist
  |
  +-- Evolus
        business-process lane powered by an open AMD-hosted model
```

The point is not “we connected many models.”

The point is:

**InnerOS knows why, when, how much, and under what authority each intelligence resource may be used.**
