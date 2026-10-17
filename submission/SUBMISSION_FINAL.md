# InnerOS — Governed AI Operations on AMD

## Tagline
**Reason. Act. Prove.**

## Short description
InnerOS is a local-first AI operations fabric that turns AMD-hosted intelligence into governed real-world action, then seals the result into verifiable evidence that can be replayed and audited.

## The problem
AI systems are increasingly capable of reasoning, but businesses still struggle with a harder question: **how do you let AI act without losing control, accountability, or proof?**

A useful operational AI system must answer:
- where the intelligence ran;
- why that runtime was selected;
- what action was proposed;
- what policy boundary applied;
- what was actually executed;
- whether the result was verified;
- whether the history can be replayed later.

## The solution
InnerOS provides the control plane between intelligence and action.

For ACT III, one end-to-end workload demonstrates that architecture:

**Bellini smart-building incident**
→ **Gemma-4-31B-IT on AMD Developer Cloud / ROCm**
→ structured **IncidentPlan**
→ **Evolus Workflow + Knowledge Library**
→ **InnerOS Evidence / Replay**

The model does not simply answer a prompt. InnerOS turns reasoning into a governed operational artifact and preserves the evidence needed to prove what happened.

## Why AMD
AMD is both an execution platform and a compute choice inside InnerOS.

The ACT III partner proof uses **AMD Developer Cloud / ROCm** with Gemma-4-31B-IT.

The broader InnerOS architecture also includes local AMD execution with Radeon AI PRO R9700, vLLM and Qwen3-Coder AWQ. Final public performance numbers for that local lane must be copied exactly from the canonical Intel benchmark JSON. No older benchmark may be substituted.

## Why Gemma
Gemma acts as the incident reasoning layer for the demonstrated workflow.

Verified state:
- model: **Gemma-4-31B-IT**
- AMD Developer Cloud endpoint: `https://developer.amd.com.cn/radeon/api/v1`
- live completion ID: `615398e579fb46e8be320f66c82e4b31`
- 12 available models discovered
- status: **LIVE_VERIFIED**

## Why Evolus
Evolus transforms model reasoning into a business workflow boundary.

Verified state:
- MCP: `https://api.evolus.ai/mcp`
- server: **Evolus2 Data Server v1.0.0**
- application: **InnerOS**
- app ID: `80dfecd4-8474-4aad-9565-5b7a2be10ea4`
- building blocks: **workflow**, **knowledge_library**
- status: **LIVE_VERIFIED**

## Evidence and replay
InnerOS produces evidence that can be checked independently from the live model call.

Verified dual-prize bundle SHA-256:

`6ee36d6905929b176fd9c49f3c1a4aa165df4a8231d5047871f581eb73b3f845`

The judge console separates:
- **LIVE**
- **LIVE VERIFIED · REPLAY**
- **MOCK**

A replay never pretends to be a fresh live request.

## Second proof: voice to governed work
InnerOS is not tied to one interface.

A connected Ambient Guardian capability demonstrates:

**Alexa / Inner Oz**
→ **InnerOS**
→ **GitHub repository + governed Ops Task**
→ **selected AI agent**
→ **AMD local execution lane**

Canonical demo repository created through that flow:

`https://github.com/Rafa-Innerchispa/inneros-alexa-amd-draftd0f`

The repo and Ops Task creation are verified. Completion of the assigned coding task must not be claimed until terminal evidence exists.

The design principle is simple:

> **Alexa does not execute infrastructure. Alexa talks to InnerOS. InnerOS decides what is allowed to happen.**

## Business value
InnerOS is intended for organizations that need AI to operate across real infrastructure without turning every model call into an unaudited black box.

Potential value:
- keep sensitive/routine workloads local when appropriate;
- use approved cloud intelligence when justified;
- preserve human approval for higher-risk actions;
- make execution history inspectable;
- provide replayable proof after the event.

A current scenario baseline estimates:
- manual baseline: **2700 s**
- active human time: **120 s**
- returned time: **2580 s**
- automation rate: **95.56%**

This is a **scenario baseline estimate**, not an independently measured productivity benchmark.

## Originality
The differentiator is not one model or one cloud endpoint.

InnerOS combines:
1. runtime/capability routing;
2. governed action;
3. human approval boundaries;
4. multi-system orchestration;
5. cryptographic evidence;
6. replay;
7. natural-language interfaces such as Alexa.

The same governance fabric can sit between multiple models, physical systems, developer tools and business workflows.

## Public demo
The public demo must expose the Judge Console or static **Verified Replay** through a real Application URL.

Preferred hostname:
`https://inneros-act3.creatorcore.ai/`

This hostname is not considered published until external HTTP 200 verification succeeds.

If Cloudflare is blocked, a zero-cost static Verified Replay may be served from GitHub Pages, with clear truth labeling.

## Technology
- AMD Developer Cloud
- ROCm
- Gemma-4-31B-IT
- Evolus MCP
- Python
- InnerOS
- evidence/replay
- local AMD Radeon AI PRO R9700
- vLLM
- Qwen3-Coder AWQ
- GitHub
- Alexa / Inner Oz connected capability

## Repository
`https://github.com/Rafa-Innerchispa/inneros-amd-act-iii`

## Application URL
**PENDING EXTERNAL HTTP VERIFICATION**

## Truth boundary
See `submission/FINAL_SOURCE_OF_TRUTH.md` and `docs/TRUTH_AND_SCOPE.md`.
