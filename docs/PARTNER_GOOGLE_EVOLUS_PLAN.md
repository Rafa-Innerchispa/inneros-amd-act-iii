# ACT III Partner Plan — Google + Evolus

## Guiding rule

Partner integrations must extend InnerOS without becoming the product story.

The core submission remains:

**InnerOS on AMD — a local-first operating fabric for governed agents, physical infrastructure, voice and verifiable execution.**

Google and Evolus are optional specialist lanes.

---

# Google

## What already exists in InnerOS

InnerOS already contains a substantial Google integration surface:

### Gemini / Vertex provider
`platform/inneros_core_runtime/gemini_runtime.py`

Capabilities include:
- governed Gemini/Vertex provider abstraction
- tool specifications with risk/approval metadata
- server-side Google credentials
- evidence storage path
- strategic-cloud routing policy

### Firestore
Existing paths support:
- Gemini evidence persistence
- agent memory mirroring

### Pub/Sub
The Gemini runtime can publish InnerOS events to a Google Pub/Sub topic.

### Model Armor
A sanitization path exists for prompts/responses with a security-required mode available.

### ADK / A2A
`google_adk_a2a.py` defines a RemoteA2aAgent-compatible contract so Google agents can be projected into the same InnerOS A2A lifecycle.

Current truth boundary: the Google Gemini ADK path is marked NON-LIVE/quota-blocked in the contract and must not be presented as a live production agent until captured evidence proves otherwise.

### AG-44 Cloud Deployer
The real AG-44 runtime is substantially more capable than its stale `agents_pool` README suggests.

It already includes:
- GCP readiness/status
- server-side GCP auth flow
- project and billing inspection
- allowlist concepts
- cloud dry-run plans
- human approval/apply gates
- Cloudflare operations
- multi-provider cloud control boundaries

ACT III work should align the agent metadata/docs with the real runtime and expose a small judge-safe Google path rather than building a second cloud platform.

## Recommended ACT III Google demo

Minimal credible flow:

1. Bellini incident is analyzed locally on AMD.
2. InnerOS produces a sanitized execution/evidence event.
3. Event is mirrored to Firestore and/or Pub/Sub.
4. Optional Gemini/Vertex specialist produces a bounded explanation/critical review.
5. InnerOS remains the authority for tool execution and approval.

This demonstrates Google without sacrificing the local-first thesis.

## Google DeepMind / Gemma update — 2026-10-14

The ACT III Discord announcement adds the missing Google-specific requirement:

- Google DeepMind is an ACT III technology partner.
- Teams using **Gemma** can compete for the dedicated Google prize.
- Gemma should run on **AMD GPUs in the cloud**, using AMD Developer Cloud / ROCm.

The event now lists a **$5,000 Google prize**.

### Recommended implementation

Do not load another large model onto the local R9700.

Use one Gemma deployment on AMD Developer Cloud as an optional InnerOS specialist lane:

`InnerOS -> governed provider adapter -> Gemma on AMD Developer Cloud / ROCm -> result -> InnerOS evidence`

Prefer to use the **same Gemma/vLLM endpoint for Evolus** so one cloud deployment supports:
- Google DeepMind / Gemma eligibility;
- Evolus main-agent model requirement;
- InnerOS cloud specialist proof.

### Token Factory facts

Official ACT III FAQ / Discord:
- event access is through `notebooks.amd.com/tokenfactory`;
- no billing or credit-card information is required there;
- the $100 AMD credit is **not required** to participate;
- API key redemption, model catalog and usage are visible after sign-in.

A dedicated vLLM endpoint may still be required for Evolus eligibility even when a shared Token Factory model API exists.

## Google partner truth boundary

Do not claim eligibility merely because GCP/Vertex exists in InnerOS. Claim the Google prize path only after:
1. Gemma is actually invoked;
2. the runtime is demonstrably AMD cloud / ROCm;
3. the run is captured in ACT III evidence.


---

# Evolus

## Why it fits InnerOS

Evolus is useful as a **business-process specialist**, not as a replacement orchestrator.

Recommended architecture:

`InnerOS -> Evolus business workflow -> structured result -> InnerOS governance/approval/evidence`

The Evolus model can run on AMD Developer Cloud, so it does not need to consume local R9700 VRAM.

## Official ACT III Evolus requirements

For partner eligibility:
1. use a free Evolus event workspace;
2. connect an open model served through the team’s own vLLM endpoint on AMD Developer Cloud;
3. use at least two Evolus building blocks;
4. drive Evolus from the app through Evolus APIs;
5. keep the app containerized, repo public and secrets in environment variables.

Recommended two building blocks:
- **Workflow**
- **Knowledge Library**

Optional third block:
- MCP connector

## Recommended Bellini business flow

Input:
- normalized Bellini incident from InnerOS

Evolus Workflow:
1. receive sanitized incident summary/evidence;
2. query a knowledge library containing sanitized runbooks/vendor guidance;
3. classify business impact and required follow-up;
4. draft a work order / escalation record;
5. return structured JSON to InnerOS.

InnerOS then:
- decides whether an action is allowed;
- asks the owner for approval when required;
- executes/coordinates the action;
- verifies outcome;
- seals evidence.

## What Rafael must do manually

These account-bound steps should not be delegated through chat:

1. Sign in at `app.evolus.ai`.
2. Create/join the ACT III event workspace using the kickoff event code.
3. Create an Evolus application/workspace agent.
4. Create an API key inside Evolus.
5. Store that API key server-side in the InnerOS owner vault / approved secret store — never paste it into Git or public chat.
6. Ensure AMD Developer Cloud / Token Factory access is available for a small open-model vLLM endpoint.

Everything after those account/secret steps can be automated by agents.

## Suggested open model

Do not load another model onto the local R9700 for Evolus.

Use a small, reliable open instruct model on AMD Developer Cloud through vLLM. Model choice should optimize:
- low setup time
- OpenAI-compatible serving
- enough reasoning for workflow/knowledge tasks
- memory footprint appropriate to the cloud allocation

The main InnerOS local model remains unchanged.

## Definition of done for Evolus

- event workspace active
- model endpoint connected
- Workflow created
- Knowledge Library created
- API adapter in ACT III repo
- one Bellini incident sent from InnerOS
- structured result returned
- human escalation/approval boundary preserved
- API calls visible in Evolus workspace statistics
- no secrets committed

---

# Priority

1. Core InnerOS/Bellini demo must remain green.
2. Google live evidence path next because most code already exists.
3. Evolus integration in parallel, isolated from production.
4. Partner failures must never block the main AMD submission.
