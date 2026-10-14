# ACT III Narrative — From One AMD GPU to InnerOS

## The real story

InnerOS did not begin as a plan to build an operating system for AI agents.

It began with an AMD Radeon AI PRO R9700.

ROCm made serious local inference practical. AMD Skills suggested something even more interesting: coding agents could consume validated, hardware-aware workflows inside tools such as Cursor and Codex.

The first idea was almost naive:

> Connect the GPU, connect the skills, connect the agents, and let them work as a team.

The GPU worked. The models worked. The skills were useful.

The team did not magically appear.

Tasks got stuck. Claims expired. Headless workers died. Repositories existed but were not safely executable. AMD and Intel nodes behaved differently. Owner approvals duplicated. An agent could finish code while coordination still believed it was running. A task could report completion without enough evidence that the objective had actually been achieved.

Those failures became the roadmap.

## InnerOS emerges

InnerOS evolved into the execution layer between **human intent, interfaces, agents, skills, compute, physical systems and evidence**.

The target operating model is now explicit:

**ChatGPT orchestrates -> local AMD/Intel Dev Swarm executes first -> Cursor, Codex and Antigravity become specialist lanes -> the owner is interrupted only when a decision deserves human attention.**

That model required building the unglamorous parts that make autonomy real:
- durable task coordination;
- Temporal + Mongo reconciliation;
- isolated worktrees;
- Project Runtime Registry;
- retries and stale-process recovery;
- claim protection between local and external agents;
- bounded tools;
- owner approvals;
- release governance;
- fail-closed evidence;
- persistent specialist memory;
- replayable execution history.

But coordination is only one layer of InnerOS.

## InnerOS is already a broader operating fabric

### VoiceOps
VoiceOps turns speech into governed execution. Voice is the interface; InnerOS owns context, routing, approval, action and evidence. The same fabric can connect AI reasoning to telephony/PBX workflows and physical operations.

### Smart buildings and Bellini
Bellini I-II became the first real demonstrative site for InnerOS Buildings.

The site contains network infrastructure, Wi-Fi, CCTV/NVR, video intercom, access control and voice systems. The original operational problem was intermittent degradation affecting multiple services. Instead of troubleshooting one camera at a time, InnerOS began reasoning about shared failure domains.

Network Guardian and Device Fabric introduced read-only observability, asset identity, service health, topology evidence and incident correlation. The AG-60 Network Engineer then evolved toward persistent site memory, governed change/verify/rollback and recovery boundaries.

Bellini is where InnerOS moved from “AI answering infrastructure questions” toward “an agent that remembers a physical environment and can progressively help operate it.”

A pilot technical-dossier workflow reduced an estimated 240–300 minutes of manual documentation to roughly 30 minutes, an estimated 87.5%–90% reduction. This remains an estimated pilot metric, not a controlled study.

### Physical Guardian
InnerOS Physical Guardian extends the same model to camera infrastructure:

`DVR/NVR/IP camera -> ingestion -> perception -> reasoning -> policy -> bounded action -> verification -> forensic evidence`

The goal is to reuse existing camera estates rather than require a full hardware replacement.

### Cloud and external specialists
InnerOS is local-first, not local-only.

Google integration already includes a governed Gemini/Vertex provider path, Firestore evidence/memory, Pub/Sub events, Model Armor and an ADK/A2A contract. AG-44 provides GCP/cloud operations with server-side credentials, read-only status, planning and human gates.

For ACT III, Evolus can become an optional business-process specialist: InnerOS keeps control while Evolus executes a business workflow on a separate open model served through vLLM on AMD Developer Cloud.

## The ACT III demonstration

The demo is one continuous story rather than a tour of unrelated screens.

An operator asks by voice what is happening in Bellini.

VoiceOps creates the intent and correlation context.

InnerOS decomposes the incident.

The Bellini/Network Engineer agent loads persistent site knowledge. Guardian and Device Fabric provide live or captured evidence. Local AMD ROCm inference reasons about the failure domain. External agents are available only when a specialist task justifies them. Optional Google/Evolus lanes receive sanitized evidence or business context without taking control away from InnerOS.

If a consequential action is proposed, InnerOS stops for owner approval.

The action is executed or safely simulated, verified, and sealed as evidence.

The operator can then inspect what happened, why a route was selected, which agent acted, which runtime was used, what changed, whether verification passed and how much human time was returned.

## What ACT III is really showing

The central claim is not that one model became smarter.

It is that **AMD compute made local intelligence practical; AMD Skills showed how agents could gain repeatable hardware-aware capabilities; real operational failures exposed everything still missing; and InnerOS became the operating fabric built in that gap.**

The R9700 did more than accelerate inference.

It changed what we believed could remain local.

And once local intelligence became practical, voice, physical infrastructure, persistent agents, cloud bridges and governed automation could all become parts of one system.

## Judge takeaway

**AMD did not merely accelerate InnerOS. AMD changed its architecture.**

From one GPU, we ended up building a local-first operating fabric for agents, voice, buildings, cloud and verifiable autonomous work.
