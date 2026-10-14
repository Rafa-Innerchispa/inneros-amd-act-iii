# InnerOS Integration Map — ACT III

## Product thesis

InnerOS is not only a multi-agent scheduler. It is the operating layer that connects interfaces, AI models, specialized agents, physical infrastructure, cloud services, governed actions and verifiable evidence.

ACT III should present the system as a layered fabric.

## 1. Human interfaces

### VoiceOps
Voice is an operational interface, not a standalone chatbot.

Canonical flow:

`human voice -> realtime speech understanding -> InnerOS Voice Gateway -> context/policy -> local-first routing -> bounded capability -> approval -> action -> evidence/replay`

VoiceOps has existing contracts for:
- session/correlation state
- explicit approval semantics
- local AMD routing
- action evidence
- Human Time Returned
- PBX/SIP integration boundaries

### WhatsApp owner control
WhatsApp is an escalation/authorization channel for decisions worth interrupting the owner.

Recent coordination work includes:
- authorization deduplication
- truthful cancellation state
- exact-task resend behavior
- owner-scoped grants

### Web/API/Alexa
InnerOS also exposes web/API surfaces and has an Ambient Guardian/Alexa integration path. These belong to the broader interface layer even when the ACT III demo focuses on voice + web evidence.

## 2. Compute fabric

### Local AMD
- AMD Radeon AI PRO R9700
- ROCm
- local vLLM/Qwen workloads
- preferred for private, latency-sensitive and infrastructure-aware reasoning

### Local Intel
- Ollama/local models
- secondary execution node
- used as failover or complementary local capacity

### AMD cloud
AMD Developer Cloud is the natural extension for event-specific workloads that should not consume the local R9700, including an optional Evolus vLLM endpoint.

### Strategic cloud providers
InnerOS has provider adapters for external cloud paths, but cloud is not the default. External compute is used when policy/capability justifies it.

For ACT III, the Google/AMD partner path uses **Gemma-4-31B-IT through AMD Token Factory** as a visible Multimodal Incident Director. It fuses VoiceOps intent, Bellini visual/topology evidence, AG-60/Device Fabric telemetry and safe shared memory into a schema-checked incident plan that InnerOS turns into governed agent/tool work.

A separate dedicated vLLM endpoint on AMD Developer Cloud may still be required for Evolus eligibility. Where practical, use Gemma there too so the same Google DeepMind open-model family spans both partner demonstrations.

Gemini 4 Argon is a separate governed InnerOS specialist for deep engineering and long-horizon tasks. It is not the ACT III Gemma prize path. Argon must remain behind InnerOS cost controls and local-first routing.

## 3. Agent fabric

### Orchestration
- ChatGPT / owner-facing orchestration
- task decomposition
- routing and escalation

### Local executors
- Dev Swarm workers
- AMD + Intel local execution
- bounded worktree/repo scope

### Specialist external lanes
- Cursor
- Codex
- Antigravity
- additional A2A/MCP specialist agents

### Domain agents
Representative specialist roles include:
- AG-60 Network Engineer
- Bellini/building operations agent
- VoiceOps agent
- cloud deployer AG-44
- GitHub/GitLab development lanes
- research/opportunity agents
- Physical Guardian agents

The design target is not “every agent can do everything”. Each agent should have bounded capabilities, persistent domain context where appropriate, and explicit evidence of work.

## 4. Coordination fabric

The hard engineering layer includes:
- durable task records
- Temporal workflows
- Mongo coordination state
- claims / leases
- retries and stale-PID recovery
- external-agent claim protection
- isolated worktrees
- Project Runtime Registry
- local/external execution lanes
- owner approvals
- fail-closed completion evidence
- release governance

Current operating model:

**ChatGPT orchestrates -> local AMD/Intel Dev Swarm executes first -> Cursor/Codex/Antigravity act as specialist lanes -> WhatsApp escalates genuine owner decisions.**

## 5. Physical-world layer

### Bellini / InnerOps Buildings
- network discovery and diagnostics
- managed/unmanaged infrastructure
- CCTV/NVR
- video intercom/access
- Wi-Fi and switching
- failure-domain reasoning
- Network Guardian
- Device Fabric
- AG-60 persistent Network Engineer

### Physical Guardian
- RTSP/ONVIF/vendor ingestion
- legacy analog cameras through DVR streams
- IP cameras
- local/edge perception
- anomaly/behavior reasoning
- governed actions
- forensic evidence

## 6. Cloud and partner layer

### Google
Existing InnerOS Google components include:
- Gemini/Vertex provider adapter
- Firestore evidence/memory paths
- Pub/Sub event path
- Model Armor sanitization path
- Google ADK/A2A contract
- AG-44 GCP operations/auth/preflight layer

Truth boundary:
- the Google ADK RemoteA2aAgent contract is not the same as a proven live Gemini agent run;
- partner eligibility should only be claimed after one live, captured Google-backed path is demonstrated.

### Evolus
Recommended ACT III role:

`InnerOS incident -> Evolus business workflow / knowledge block -> structured result -> InnerOS approval/evidence`

Evolus should remain a specialist business-process lane, not the InnerOS orchestrator.

Use **Workflow + Knowledge Library** as the minimum two Evolus building blocks. The preferred model is the same **Gemma on AMD Developer Cloud / ROCm** used for the Google partner proof, minimizing duplicate infrastructure and avoiding local R9700 VRAM pressure.

### Cognee shared memory

Cognee is **not an official ACT III prize partner**, but it is already a real InnerOS product capability validated in `Rafa-Innerchispa/inneros-personal-brain`.

Existing reusable surfaces include:
- Cognee Cloud direct recall/remember;
- canonical dataset `inneros-personal-brain`;
- official Cognee MCP;
- direct Strands memory tools;
- Codex, Cursor and Antigravity shared-memory routes;
- VoiceOps verified-outcome memory bridge.

ACT III should use this existing fabric to prove:
`Agent A learns -> Agent B remembers`

For Bellini/AG-60, only curated safe facts/decisions/outcomes should enter Cognee. Private operational context, secrets and customer-sensitive payloads remain in InnerOS private memory (Mongo/Qdrant).

## 7. Trust and audit layer

InnerOS is designed to preserve:
- runtime identity
- route reasons
- timestamps
- output hashes
- approval evidence
- execution artifacts
- verification results
- rollback/LKG concepts
- replayable historical evidence
- Human Time Returned

The product principle is:

**Autonomy should increase without making actions less visible.**

## 8. ACT III demonstration composition

One demo can expose most of InnerOS without turning into a feature checklist:

1. Operator asks by voice about a Bellini incident.
2. VoiceOps normalizes intent.
3. InnerOS creates/coordinates tasks.
4. Bellini/Network Engineer agent retrieves persistent site context.
5. Guardian/Device Fabric provide evidence.
6. Local AMD inference and domain agents prepare the evidence bundle.
7. Gemma-4-31B-IT on AMD Token Factory acts as Multimodal Incident Director and returns a structured plan with hypotheses, evidence references, required tools and delegated tasks.
8. InnerOS dispatches those bounded tasks to AG-60 / Guardian / other specialists; optional Argon is reserved for unusually hard engineering work, not routine incident handling.
9. Evolus can turn the verified technical result into the business workflow/work order.
10. InnerOS requests approval before a consequential action.
11. Action is executed or safely simulated.
12. Verification confirms outcome.
13. Evidence/replay shows exactly what happened.
14. Human Time Returned quantifies operational value.

This is a single story that demonstrates the whole operating fabric instead of showing disconnected product modules.
