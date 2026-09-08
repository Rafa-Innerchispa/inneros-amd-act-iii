# Architecture

## Goal

InnerOS AMD ACT III is an auditable local-first execution fabric for autonomous agents across AMD edge and cloud compute.

## Core flow

1. A workflow creates one or more agent tasks.
2. The router evaluates privacy, latency, cost, capability, context length and availability.
3. The task is routed to local AMD ROCm or AMD cloud compute.
4. Execution emits structured routing and decision evidence.
5. Metrics are recorded as MEASURED or ESTIMATED.
6. Evidence artifacts are hashed with SHA-256.
7. Audit Replay verifies a historical execution without live refresh or side effects.

## Components

- Workflow ingress
- Capability router
- AMD local adapter
- AMD cloud adapter
- MCP/A2A-compatible agent runtime
- Evidence recorder
- Offline replay verifier
- Human Time Returned metrics

## Truth states

PROVEN, PARTIAL, CONTRACT-ONLY, PLANNED.

## Intended ACT III demo

A task graph visibly routes work to AMD local or AMD cloud targets, displays reason codes and metrics, and lets judges open an evidence bundle and verify/replay a run offline.
