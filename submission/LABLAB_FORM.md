# LabLab Submission Form — ACT III

Status: **READY TO FILL / ASSETS IN PROGRESS**

Internal deadline: **October 17, 2026**  
Reason: LabLab's live dashboard currently describes the online build window as October 12–17, while the main event page shows October 12–18 including the on-site phase. We use October 17 as the safe submission deadline.

## Basic information

### Project title
**InnerOS AMD Sovereign Agent Fabric**

### Short description
InnerOS began with one AMD GPU and a simple idea: give coding agents AMD Skills and local ROCm compute, then let them work as a team. The failures of that experiment became a local-first agent operating layer that coordinates AMD/Intel workers, specialist agents, approvals, recovery and replayable evidence.

### Long description
InnerOS did not begin as a plan to build an operating system for AI agents.

The catalyst was an AMD Radeon AI PRO R9700.

With local ROCm compute available, serious AI workloads no longer had to depend entirely on remote providers. At the same time, ROCm.AI and AMD Skills showed a compelling new model: coding agents such as Cursor and Codex could consume validated AMD workflows directly inside the tools developers already use.

The first idea sounded simple: connect the skills, connect the agents, connect the local GPU, and let them work together.

That was the beginning of InnerOS.

The models could reason. The GPU could run them. Skills could teach hardware-aware workflows. But the agents were still not a reliable team. Tasks could be created and never claimed. Leases expired. Headless processes died. Local AMD and Intel paths behaved differently. Repositories existed but were not always safely executable. Owner authorization could duplicate. An agent could finish work while the coordination layer still believed it was running.

Those failures became the product roadmap.

InnerOS evolved into the missing execution layer between human intent, skills, agents and compute.

Today the system is moving toward a simple operating model:

**ChatGPT orchestrates. Local Dev Swarm workers execute first across AMD and Intel. Cursor, Codex and Antigravity become specialist external lanes. The owner is interrupted only when a decision deserves human attention.**

Underneath that model are the less glamorous systems that make autonomy real: durable coordination, Temporal/Mongo reconciliation, isolated worktrees, Project Runtime Registry, bounded execution, owner-scoped approvals, fail-closed evidence, retry/recovery logic, local release governance and replayable execution receipts.

ACT III turns that journey into one concrete Intelligent Industry demonstration.

A smart-building incident reports intermittent degradation in cameras or intercom video. InnerOS decomposes the problem, assigns specialized agents and skills, correlates telemetry, retrieves topology and prior evidence, plans a bounded remediation and keeps privacy- or latency-sensitive reasoning on local AMD ROCm compute. Any mutating action requires explicit human approval. The system then verifies the outcome and seals the run with runtime identity, route reasons, timestamps, hashes and Human Time Returned.

The central claim is not that one model became smarter.

It is that **AMD compute made local intelligence practical, AMD Skills showed how agents could gain repeatable hardware-aware capabilities, and discovering why those pieces were not magically enough forced us to build the coordination fabric that became InnerOS.**

The R9700 did more than accelerate inference.

It changed the architecture of the project.

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
