# ACT III Flagship Demo Scenario

## Purpose

The flagship ACT III story is not a generic chat demo. It is a bounded,
auditable incident-response workflow for physical infrastructure.

The current runner is **CONTRACT-ONLY**. It exists to freeze the workflow,
evidence schema and judge-facing story before the live InnerOS adapters are
connected. It does not claim that synthetic steps are live production actions.

## Scenario

A building reports intermittent camera/intercom video degradation.

The workflow:

1. incident intake normalizes the human report;
2. a network guardian correlates telemetry;
3. a knowledge agent retrieves topology and prior evidence;
4. a repair planner proposes the lowest-risk remediation and rollback;
5. an executor can perform a bounded mutation only with explicit approval;
6. an evidence verifier seals the result for replay.

Every step records:

- agent
- skill
- route target
- route reason codes
- output hash
- Human Time Returned estimate
- mutation/approval boundary

## Why AMD matters

The scenario is local-first. Private building telemetry and operational context
are routed to the local AMD ROCm target by policy. Cloud routing remains an
explicit contract path for elastic work, never an invisible fallback.

The live demo must replace synthetic runtime identity and timings with measured
AMD evidence before they are described as proven hackathon results.

## Run

```bash
python -m inneros_act3.scenario
```

The command emits a deterministic JSON scenario receipt plus a SHA-256 evidence
manifest.

## Live integration gates

Before final judging:

- [ ] replace synthetic telemetry with one real InnerOS incident input;
- [ ] bind at least one real skill invocation;
- [ ] record actual AMD model/runtime identity;
- [ ] record actual elapsed time and VRAM/throughput where relevant;
- [ ] demonstrate explicit approval before any mutating action;
- [ ] emit a replayable evidence bundle;
- [ ] show the same run in the judge-facing timeline/UI;
- [ ] label all estimated business metrics as ESTIMATED until measured.

## Fallback

If a live external system is unavailable during judging, replay the previously
sealed evidence bundle. The fallback must be visibly labeled as replay, not a
live execution.
