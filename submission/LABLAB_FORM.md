# LabLab Submission Form — ACT III

Status: **READY TO FILL / ASSETS IN PROGRESS**

Internal deadline: **October 17, 2026**  
Reason: LabLab's live dashboard currently describes the online build window as October 12–17, while the main event page shows October 12–18 including the on-site phase. We use October 17 as the safe submission deadline.

## Basic information

### Project title
**InnerOS AMD Sovereign Agent Fabric**

### Short description
InnerOS is a local-first agentic compute fabric on AMD ROCm that routes autonomous workloads across local and cloud AMD infrastructure, coordinates specialized agents and skills, and produces replayable evidence for every execution.

### Long description
Autonomous AI agents are becoming capable of real work, but most agent platforms still hide the operational details that matter in production: where each task runs, why a route was selected, which tool or skill acted, what changed, how long it took, and whether the result can be independently verified later.

InnerOS AMD Sovereign Agent Fabric turns those hidden decisions into part of the product.

A user request enters the InnerOS control plane and is decomposed into bounded tasks. Capability and policy routing decide which specialized agent and skill should execute each task and whether the workload should remain on local AMD ROCm infrastructure or use an approved AMD cloud path. Local execution is preferred for privacy, latency and sovereignty. Every route emits structured reason codes and runtime identity.

For ACT III, the flagship demonstration is a smart-building infrastructure incident. InnerOS receives a degradation report affecting cameras or intercom video, correlates telemetry, retrieves topology and previous evidence, builds a bounded remediation plan, requires human approval before any mutating action, verifies the outcome and seals the complete run as replayable evidence.

The AMD stack is not decorative. Local inference runs on AMD hardware with ROCm, using local Qwen/vLLM workloads. The system is designed around real execution constraints: hardware availability, routing policy, failover, observability, agent coordination and measurable business value.

The final evidence bundle records runtime identity, route reasons, timestamps, output hashes and Human Time Returned. Historical runs can be verified and replayed without silently refreshing external state.

InnerOS therefore demonstrates a different idea of agentic infrastructure: not simply an AI that can answer, but an execution fabric that can show where the work ran, why it ran there, what it did and whether the result can still be trusted later.

### Technology tags
- AMD ROCm
- AMD GPUs
- vLLM
- Qwen
- Agentic AI
- MCP
- A2A
- Skills
- Multi-agent systems
- Local-first AI
- Edge AI
- Smart Buildings
- Observability
- Forensic Replay

### Suggested categories
- Agent Builder
- Intelligent Industry
- Developer Tools
- Infrastructure / Operations

## Repository and hosting

### Public GitHub repository
https://github.com/Rafa-Innerchispa/inneros-amd-act-iii

Status: **PASS — repository is public**

### Demo platform
**PENDING FINAL LIVE DEMO**

Preferred:
- InnerOS / ACT III judge-facing demo UI
- AMD local runtime on Radeon AI PRO R9700
- approved AMD cloud path only where actually demonstrated

### Application URL
**PENDING**

Do not submit a placeholder URL. Add only after public HTTPS verification.

## Cover image

Status: **PENDING**

Creative brief:
A clean dark technical composition showing InnerOS at the center routing agent workloads between a local AMD ROCm edge node and AMD cloud compute. Include a subtle smart-building/network incident context, evidence trail and replay concept. Avoid generic robot imagery and avoid unsupported AMD branding claims.

## Video presentation

Status: **SCRIPT READY / RECORDING PENDING**

Target length: approximately 3 minutes.

Source script:
`submission/VIDEO_SCRIPT.md`

Required live proof:
1. real task enters InnerOS;
2. agents/skills are visible;
3. local AMD ROCm route is visible;
4. reason codes/runtime identity are shown;
5. smart-building workflow produces a bounded recommendation/action;
6. evidence bundle is opened;
7. replay verifies the historical run;
8. Human Time Returned closes the business story.

## Slide presentation

Status: **OUTLINE READY / DECK PENDING**

Source:
`submission/SLIDE_DECK_OUTLINE.md`

## Judging alignment

### Application of Technology
- AMD ROCm is part of the execution fabric, not a detached benchmark.
- local model execution is used for private/latency-sensitive workloads.
- routing and runtime identity are visible in evidence.

### Presentation
- one flagship smart-building scenario;
- one visual task timeline;
- one local/cloud routing view;
- one evidence/replay view;
- one business-value view.

### Business Value
- reduced operator investigation time;
- local-first privacy and sovereignty;
- controlled remediation;
- lower manual coordination overhead;
- measurable Human Time Returned.

### Originality
The differentiator is the combination of:
- policy-aware workload placement;
- specialized agents + skills;
- AMD edge/cloud execution;
- bounded actions;
- machine-readable evidence;
- offline forensic replay;
- business-value measurement.

## Originality boundary

Pre-hackathon baseline is documented in:
`docs/PRE_HACKATHON_BASELINE.md`

Hackathon-period work is tracked from the frozen baseline and must be described accurately as:
- pre-existing;
- integrated during ACT III;
- newly built during ACT III.

## Final submission blockers

- [ ] public demo URL
- [ ] cover image
- [ ] 3-minute video
- [ ] slide deck
- [ ] live AMD runtime evidence
- [ ] one end-to-end smart-building run
- [ ] measured latency/runtime evidence
- [ ] replay verification
- [ ] Human Time Returned screenshot/metric
- [ ] final proofread against actual demonstrated capabilities
