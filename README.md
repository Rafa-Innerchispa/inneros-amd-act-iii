# InnerOS Labs — AMD Developer Hackathon ACT III

**Local-First Agentic Infrastructure on AMD**

InnerOS Labs is building an auditable, local-first agentic compute fabric that can orchestrate autonomous AI workloads across AMD edge hardware and AMD cloud infrastructure.

## Hackathon thesis

Most agent systems treat compute as an invisible backend. InnerOS makes compute placement, routing, evidence and replay first-class parts of the product.

The ACT III entry will focus on a reproducible demonstration where autonomous agents can:

- run locally on AMD ROCm hardware;
- route selected workloads to AMD cloud capacity when policy or capability requires it;
- execute multiple tasks concurrently;
- expose routing reasons, latency, throughput and cost-related evidence;
- preserve decision evidence for every run;
- replay historical runs without silently refreshing the world state;
- quantify Human Time Returned on real workflows.

## Proposed architecture

```text
User / Workflow
      |
      v
InnerOS Control Plane
      |
      +--> Policy + Capability Router
      |        |
      |        +--> AMD Edge / Local ROCm
      |        +--> AMD Cloud Compute
      |
      +--> Multi-Agent Execution
      |
      +--> Decision Evidence
      +--> Human Time Returned
      +--> Forensic Replay
```

## Existing pre-hackathon building blocks

This repository intentionally separates the ACT III submission from pre-existing InnerOS components. Existing work may be integrated through documented interfaces rather than copied blindly into the hackathon repository.

Current pre-hackathon building blocks include:

- InnerOS agentic control plane;
- local execution plane;
- model/capability routing;
- Qwen + vLLM serving on AMD ROCm;
- experimental R9700 / HyperLoom compatibility and concurrency work;
- Decision Evidence schemas;
- Human Time Returned instrumentation design;
- Forensic Replay / Evidence Bundle work;
- MCP and A2A communication layers.

See [`docs/PRE_HACKATHON_BASELINE.md`](docs/PRE_HACKATHON_BASELINE.md) for the formal baseline boundary.

## ACT III target demonstration

A user launches a complex workflow. InnerOS decomposes the work into agent tasks, evaluates privacy/capability/load policy, executes tasks on AMD local or cloud resources, records why each route was chosen, measures the result, and produces a replayable evidence bundle.

The visible demo should make the edge-to-cloud path understandable in seconds, not require judges to reverse-engineer six terminals and a prayer.

## Repository structure

```text
docs/          Architecture, baseline and technical notes
submission/    LabLab copy, judging notes, metrics and demo script
src/           ACT III-specific implementation
benchmarks/    Reproducible performance and routing measurements
tests/         Functional and evidence verification
```

## Guiding constraints

- Local-first by default.
- AMD-first execution path for the submission.
- Measured claims must remain distinguishable from estimates.
- Existing capabilities must be labeled as pre-hackathon baseline.
- New ACT III work must be attributable to the submission period.
- No benchmark claim without machine-readable evidence.
- No cloud dependency when a local path can perform the task adequately.

## Status

Pre-hackathon preparation. Tracks and final implementation scope will be adjusted once AMD/LabLab publish the complete ACT III challenge details.

## License

MIT. See [`LICENSE`](LICENSE).
