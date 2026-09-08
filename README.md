# InnerOS Labs — AMD Developer Hackathon ACT III

**Local-First Agentic Infrastructure on AMD**

InnerOS AMD ACT III is an auditable local-first agentic compute fabric designed to route autonomous AI workloads across AMD edge and cloud infrastructure while preserving the evidence needed to understand, verify and replay every execution.

## One-line pitch

> An auditable local-first agentic compute fabric that routes autonomous AI workloads across AMD edge and cloud GPUs, records why each decision was made, and makes every run replayable.

## Why this project exists

Most agent demos show what a model answered. InnerOS aims to show **where the work ran, why it ran there, what the agent saw, what it did, how long it took, what it cost, and whether the execution can be independently verified later**.

That turns AI infrastructure from a black box into an inspectable execution fabric.

## Target AMD stack

- AMD ROCm
- local AMD GPU execution
- vLLM + Qwen workloads
- AMD Developer Cloud for elastic execution
- multi-agent orchestration through MCP/A2A-compatible boundaries
- machine-readable performance and routing evidence

Exact ACT III cloud hardware and track-specific AMD technologies will be recorded after the official tracks and access details are published.

## Architecture

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

See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).

## Current seed implementation

The repository already contains a dependency-light Python reference core that demonstrates:

- local-first routing;
- privacy fail-closed behavior;
- elastic-capacity routing to cloud;
- availability fallback;
- structured routing reason codes;
- canonical evidence serialization;
- SHA-256 evidence verification;
- deterministic unit tests;
- GitHub Actions CI.

This seed is intentionally provider-neutral before ACT III. The hackathon-period work will connect the core to the final AMD local/cloud runtime and visual demo.

## Run it

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
python -m inneros_act3.demo
```

## Pre-hackathon originality boundary

This repository is being prepared before ACT III. Existing InnerOS capabilities are documented separately in [`docs/PRE_HACKATHON_BASELINE.md`](docs/PRE_HACKATHON_BASELINE.md).

Immediately before kickoff we will freeze the exact baseline SHA/tag. Final submission claims will distinguish:

- **pre-existing** building blocks;
- **integrated during ACT III** capabilities;
- **newly built during ACT III** features.

Experimental AMD compatibility will not be described as official upstream support unless that becomes factually true.

## Success criteria

A strong final demo should prove:

1. a real workload runs on AMD infrastructure;
2. workloads can route between local AMD and AMD cloud based on policy/capability;
3. routing reasons are captured in structured evidence;
4. execution metrics are measured and machine-readable;
5. historical evidence can be verified offline;
6. a multi-agent workflow works end to end;
7. the visual UI makes edge-to-cloud movement understandable in seconds;
8. business value is visible through Human Time Returned, cost and quality metrics.

## Repository map

```text
src/inneros_act3/           routing + evidence seed
tests/                      deterministic tests
docs/ARCHITECTURE.md        working architecture
docs/PRE_HACKATHON_BASELINE.md
                            originality boundary
docs/ROADMAP.md             execution plan
submission/PROJECT_DESCRIPTION.md
                            LabLab copy draft
submission/DEMO_CHECKLIST.md
                            judge/demo checklist
submission/VIDEO_SCRIPT.md  3-minute video draft
.github/workflows/ci.yml     CI
```

## Current event state

ACT III is scheduled for October 2026. The official LabLab page currently lists the judging dimensions as **Application of Technology, Presentation, Business Value and Originality**. Tracks are still TBA as of this pre-hackathon preparation phase, so the project is intentionally not locked to one track yet.

Official event page: https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-iii

## Truth boundary

Project claims use explicit evidence states:

- **PROVEN** — reproduced with evidence;
- **PARTIAL** — some acceptance criteria remain;
- **CONTRACT-ONLY** — interface exists, live integration not proven;
- **PLANNED** — design only.

No benchmark claim is considered proven without reproducible evidence.

## Team

**InnerOS Labs**  
Building local-first, auditable agentic infrastructure.

## License

MIT. See [`LICENSE`](LICENSE).
