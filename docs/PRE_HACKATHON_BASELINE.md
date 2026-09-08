# Pre-Hackathon Baseline

Snapshot date: 2026-09-07

This document exists to preserve a clean originality boundary for AMD Developer Hackathon ACT III.

## Existing before the official ACT III build window

- InnerOS agentic control plane
- local execution plane and repo-scoped execution policies
- MCP and A2A communication layers
- capability/model routing concepts and implementation work
- Qwen served through vLLM on AMD ROCm infrastructure
- experimental Radeon AI PRO R9700 / gfx1201 compatibility and concurrency research
- HyperLoom-related experimental compatibility work in a separate repository
- Decision Evidence schema/design work
- Forensic Replay / Evidence Bundle work in a separate repository
- Human Time Returned measurement design

These are pre-existing building blocks. They may be integrated, adapted, or measured during ACT III, but must not be misrepresented as newly invented during the hackathon.

## Work intended for ACT III

The final set will depend on the official tracks. Candidate hackathon-period work includes:

- ACT III-specific AMD edge/cloud router integration
- AMD Developer Cloud adapter and deployment path
- unified visual task graph for local/cloud execution
- benchmark harness comparing routing/concurrency modes
- end-to-end evidence viewer and offline replay flow
- hackathon-specific demo workflow and UI
- reproducible deployment/package for judges

## Freeze procedure

Immediately before kickoff:

1. record the main branch SHA;
2. create a signed or annotated baseline tag if available;
3. archive this baseline document with the exact SHA;
4. start ACT III work on a dedicated branch;
5. track every new feature and benchmark against that baseline.

## Claim policy

No result is PROVEN without reproducible evidence. Experimental compatibility is not official upstream support. Serving/concurrency improvements must not be described as kernel-level optimization unless directly measured and attributable.
