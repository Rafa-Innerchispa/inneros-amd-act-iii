# ACT III Slide Deck Outline

Target: **7 slides, judge-friendly, visual first**

## Slide 1 — InnerOS AMD Sovereign Agent Fabric
**Subtitle:** Local-first agentic infrastructure that can explain and replay its own work.

Visual:
- InnerOS center
- AMD local ROCm node
- AMD cloud node
- agents/skills around control plane

One sentence:
Autonomous work is useful only if you can see where it ran, why it ran there and what it actually did.

## Slide 2 — The production problem
Three problems:
1. agent systems hide compute placement;
2. actions are hard to audit after the fact;
3. sensitive operations should not silently leave local infrastructure.

Visual:
black-box agent vs inspectable InnerOS path.

## Slide 3 — The InnerOS execution fabric
Flow:
User request → capability/policy router → agents + skills → AMD local/cloud execution → evidence → replay.

Callouts:
- local-first
- bounded actions
- failover
- routing reason codes
- MCP / A2A compatible

## Slide 4 — Flagship use case: smart-building incident
Scenario:
camera/intercom degradation → telemetry correlation → topology retrieval → remediation plan → human approval → bounded action → verification.

Show six-step timeline from `docs/DEMO_SCENARIO.md`.

## Slide 5 — Why AMD
Show only proven/runtime-backed claims:
- AMD Radeon AI PRO R9700 local node
- ROCm
- local Qwen/vLLM inference
- AMD cloud path where demonstrated

Metrics panel:
- runtime identity
- latency
- VRAM / throughput where measured
- local vs cloud route

## Slide 6 — Evidence, replay and trust
Show:
- execution manifest
- SHA-256 bundle
- route reasons
- output hash
- forensic replay

Message:
The system does not just log an answer. It preserves the execution boundary needed to verify the run later.

## Slide 7 — Business value
Metrics:
- Human Time Returned
- automation rate
- operator investigation time
- local/cloud split
- bounded remediation

Close:
**AMD provides the compute. InnerOS makes autonomous execution local-first, inspectable and replayable.**

## Deck truth rules
- no synthetic metric shown as measured;
- no AMD hardware claim without runtime evidence;
- label replay clearly;
- distinguish pre-existing platform components from ACT III integrations.
