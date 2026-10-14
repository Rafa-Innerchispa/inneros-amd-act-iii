# Origin Story — From One AMD GPU to InnerOS

## The spark

InnerOS did not begin as a plan to build an agent operating system.

The catalyst was an AMD GPU.

With a Radeon AI PRO R9700 available locally, ROCm made it possible to run serious AI workloads without sending every request to a remote provider. Around the same time, ROCm.AI and AMD Skills made a compelling promise: AI coding agents could consume AMD-authored, validated workflows directly inside the tools developers already use.

The first idea was simple:

> If Cursor, Codex and other agents can see AMD Skills, perhaps we can connect them to local ROCm compute and let them work as a team.

That idea was directionally right.

It was also nowhere near enough.

## What the GPU made possible

The AMD node changed the economics and architecture of the project.

Instead of treating local inference as a fallback, it could become the default execution layer for private, latency-sensitive and infrastructure-aware work.

Local Qwen/vLLM workloads could live close to:
- operational telemetry;
- source code;
- device state;
- internal knowledge;
- automation tools;
- building/network infrastructure.

That made a local-first agent fabric technically credible.

## What Skills did — and did not — solve

AMD Skills solved an important layer: they could give an AI coding agent validated knowledge and repeatable AMD workflows.

But a skill is not an operating system.

Connecting an agent to a skill did not answer:

- Which agent owns a task?
- How is a task claimed?
- What happens if an agent dies halfway through?
- How do local and external agents share work?
- How do AMD and Intel nodes fail over?
- How are branches and worktrees isolated?
- Who is allowed to mutate production?
- How does the owner approve an expensive or risky action?
- How do we prove that an action really happened?
- What happens when Temporal and Mongo disagree?
- How do we distinguish a real completion from a stale process?
- How do we replay what happened later?

Those missing layers became the real engineering problem.

## The uncomfortable middle

The first multi-agent experiments exposed failure modes that normal demos conveniently avoid.

Tasks could be created but never claimed.

External agents could hold stale leases.

A headless process could die while the coordination layer still believed it was working.

A task could claim success without objective evidence.

The same action could trigger duplicate owner authorization messages.

Local AMD and Intel execution were not initially symmetric.

A repository could exist in GitHub but still be impossible for the local execution plane to hydrate or modify safely.

Each problem looked small in isolation.

Together, they described the missing product.

## InnerOS emerges

InnerOS became the control plane between human intent, agents, skills and compute.

Recent platform work turned those failures into explicit platform capabilities:

- durable task coordination;
- Temporal + Mongo reconciliation;
- Project Runtime Registry;
- isolated worktrees;
- fail-closed evidence gates;
- bounded local execution;
- automatic Dev Swarm workers;
- local AMD / Intel symmetry;
- external-agent claim protection;
- owner-scoped grants;
- headless retry and stale-PID recovery;
- Last Known Good / rollback concepts;
- governed local release execution;
- WhatsApp owner authorization;
- persistent specialist-agent memory;
- replayable execution evidence.

The current execution model is now explicit:

> ChatGPT orchestrates. Local Dev Swarm workers execute first across AMD and Intel. Cursor, Codex and Antigravity are specialist external lanes. The owner is interrupted only when a decision is genuinely worth escalating.

This is still being hardened, but it is no longer an architecture diagram. It is a working coordination system being tested by the same projects submitted to the hackathon.

## Why ACT III is the right place to tell this story

ACT III is not a separate demo built next to InnerOS.

ACT III is the point where the journey becomes visible.

The project shows how access to AMD compute changed the system from cloud-dependent assistants into a local-first execution fabric.

The flagship smart-building incident demonstrates the result:

1. a real operational problem enters InnerOS;
2. the control plane decomposes it;
3. agents and skills are selected;
4. local AMD ROCm execution is preferred;
5. external specialists can be invoked when justified;
6. mutating actions remain bounded by owner approval;
7. every route and output produces evidence;
8. the run can be verified and replayed later.

## The real thesis

The R9700 did more than make inference faster.

It changed what we believed could remain local.

AMD Skills did more than provide instructions.

They exposed the possibility of giving agents repeatable, hardware-aware capabilities.

The failures that followed exposed everything still missing between a capable agent and an autonomous operating environment.

InnerOS is the system we had to build in that gap.

## One-sentence version

**A single AMD GPU gave us enough local intelligence to try building a team of autonomous agents; discovering why that was not magically enough is what created InnerOS.**
