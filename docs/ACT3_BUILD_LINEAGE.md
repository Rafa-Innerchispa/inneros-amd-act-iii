# ACT III Build Lineage

This document explains exactly what InnerOS brought into AMD Developer Hackathon ACT III, what was reused or adapted, and what was built or integrated specifically for the hackathon.

The goal is to make the originality boundary explicit.

## 1. Pre-existing InnerOS foundation

The following capabilities existed before the ACT III build window and were **not invented during this hackathon**:

- InnerOS agentic control plane.
- Local execution plane and repo-scoped execution policies.
- MCP and A2A communication layers.
- Capability/model routing concepts and implementation.
- Qwen served through vLLM on AMD ROCm infrastructure.
- Experimental Radeon AI PRO R9700 / gfx1201 compatibility and concurrency research.
- Decision Evidence schema/design.
- Forensic Replay / Evidence Bundle work.
- Human Time Returned measurement design.
- General multi-agent orchestration work.
- Existing real-world operational context from InnerOS deployments, including Bellini as an infrastructure workload.

These components are the foundation on top of which the ACT III submission was built.

## 2. Reused and adapted for ACT III

ACT III intentionally reuses the mature pieces of InnerOS instead of rebuilding them for a demo.

Reused/adapted components include:

### InnerOS governance and control plane
Used to preserve:
- policy boundaries;
- runtime routing;
- approval semantics;
- truth labels;
- task/evidence lineage.

### Evidence and replay
Existing evidence concepts were adapted into the ACT III partner pipeline so the final Gemma/Evolus run can be inspected and replayed.

### Local AMD execution
The existing Radeon AI PRO R9700 + ROCm + vLLM + Qwen3-Coder local lane is reused as proof that the broader InnerOS compute fabric can execute workloads locally on AMD hardware.

Final ACT III numbers must come only from the canonical N=20 benchmark JSON.

### Bellini operational context
Bellini is reused as the real-world workload/domain context for the ACT III demonstration.

ACT III does not claim Bellini itself was created for the hackathon. The hackathon-specific work is the AI reasoning, workflow, evidence and judge-facing integration around that workload.

## 3. Built or integrated specifically during ACT III

The following items represent the main ACT III-specific work:

### AMD Developer Cloud + Gemma integration
Built/integrated during ACT III:
- AMD Developer Cloud runtime path;
- Gemma-4-31B-IT discovery and live inference;
- provider integration and credential boundary;
- structured incident reasoning output;
- LIVE_VERIFIED provider evidence.

Verified completion:
- model: Gemma-4-31B-IT;
- 12 models discovered;
- live completion ID: 615398e579fb46e8be320f66c82e4b31.

### Structured IncidentPlan
The hackathon demo converts Bellini operational input into a structured IncidentPlan with:
- diagnosis;
- severity;
- recommendations;
- execution boundaries.

This is the contract between AI reasoning and downstream operational workflow.

### Evolus integration
Built/integrated during ACT III:
- live Evolus MCP transport;
- InnerOS application binding;
- Workflow building block;
- Knowledge Library building block;
- business work-order representation from the governed IncidentPlan.

Verified application:
- InnerOS;
- app ID: 80dfecd4-8474-4aad-9565-5b7a2be10ea4.

### End-to-end partner pipeline
ACT III joins the components into one judgeable path:

Bellini
→ Gemma on AMD
→ IncidentPlan
→ Evolus
→ InnerOS Evidence / Replay.

The integrated partner proof suite reached 28/28 PASS.

### ACT III evidence bundle
The partner run is sealed into an ACT III-specific replayable evidence bundle.

Canonical dual-prize bundle SHA-256:

6ee36d6905929b176fd9c49f3c1a4aa165df4a8231d5047871f581eb73b3f845

### Judge Console
Built for ACT III:
- judge-facing visual experience;
- LIVE / LIVE VERIFIED REPLAY / MOCK truth states;
- IncidentPlan visualization;
- Evolus work-order representation;
- SHA-256 evidence receipt;
- replay flow;
- judge-focused narrative and status pills.

### Submission and deployment package
Built for ACT III:
- Docker/run path for Judge Console;
- static Verified Replay preparation;
- public Application URL deployment work;
- Cloudflare/GitHub Pages delivery path;
- final README;
- submission copy;
- video narrative;
- pitch deck;
- cover direction;
- truth/scope documentation.

## 4. Technology built in the parallel Alexa hackathon and reused by ACT III

A second hackathon was being developed in parallel: Ambient Guardian / Alexa.

That work is **not claimed as ACT III-native code**.

Instead, ACT III demonstrates that InnerOS is a reusable platform whose capabilities can be accessed through a second real interface.

The Alexa hackathon built/integrated:

- Inner Oz Alexa Custom Skill;
- real InnerOS and Home Assistant queries;
- solar/grid/battery/voltage information;
- outage/restoration alerts;
- governed UniFi restart flow;
- owner approval through WhatsApp;
- post-action verification;
- voice programming dispatch;
- voice request → GitHub repository;
- voice request → governed InnerOS Ops Task.

ACT III reuses this as a connected capability:

Alexa / Inner Oz
→ InnerOS
→ GitHub + Ops Task
→ selected agent
→ AMD local execution lane.

Canonical voice-created ACT III demo repository:

https://github.com/Rafa-Innerchispa/inneros-alexa-amd-draftd0f

Important truth boundary:

- ACT III does not duplicate Ambient Guardian code.
- ACT III does not claim Alexa was built entirely inside ACT III.
- ACT III demonstrates that the same InnerOS governance fabric can be used by a real voice interface developed in parallel.

## 5. What is still engineering track / not claimed as finished ACT III work

The following are not presented as completed hackathon results unless exact final evidence proves them:

- 4/8 simultaneous agent concurrency;
- broad autonomous multi-agent scaling;
- Google voice/home integration;
- generalized telephony control;
- unrestricted programming by voice;
- measured watt-efficiency claims;
- zero-cloud operation;
- universal Human Time Returned metrics.

These remain architecture or engineering tracks.

## 6. Judge-friendly summary

### What existed before
**InnerOS foundation**
- orchestration;
- local AMD compute;
- governance;
- routing;
- evidence/replay concepts;
- real operational workloads.

### What ACT III added
**A complete AMD partner proof**
- AMD Developer Cloud;
- Gemma live reasoning;
- structured IncidentPlan;
- Evolus business workflow;
- integrated evidence bundle;
- Judge Console;
- public demo/submission package.

### What ACT III reused from the parallel Alexa hackathon
**A real natural-language interface**
- Alexa / Inner Oz;
- governed action model;
- voice-to-GitHub;
- voice-to-Ops Task.

### Why this matters
ACT III is not a collection of unrelated integrations.

It demonstrates that **InnerOS is the reusable platform layer** connecting:
- AMD compute;
- AI reasoning;
- business workflows;
- physical operations;
- developer agents;
- natural voice interfaces;
- governance and proof.

## 7. One-line originality statement

> **We did not rebuild InnerOS for the hackathon. We used ACT III to prove that an existing governed AI operations fabric could integrate new AMD-hosted intelligence, new partner workflows and new human interfaces into one auditable execution system.**
