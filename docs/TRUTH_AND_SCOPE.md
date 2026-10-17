# Truth and Scope

InnerOS ACT III uses explicit truth states because a polished demo is useless if the claims collapse under one judge question.

## States

- **LIVE_VERIFIED** — real external/provider execution with evidence.
- **VERIFIED** — reproducible proof exists, but not necessarily a fresh external call.
- **LIVE_VERIFIED_REPLAY** — replay of a previously verified live execution.
- **MOCK** — deterministic demonstration only.
- **PENDING** — required proof has not been collected yet.
- **ENGINEERING_TRACK** — architecture/work in progress, not final demonstrated capability.

## Proven today

### Gemma
**LIVE_VERIFIED**
- Gemma-4-31B-IT
- AMD Developer Cloud / ROCm
- completion ID `615398e579fb46e8be320f66c82e4b31`

### Evolus
**LIVE_VERIFIED**
- real MCP transport
- InnerOS application
- workflow + knowledge_library

### Evidence replay
**VERIFIED / REPLAYABLE**
- dual bundle SHA-256 recorded in final source-of-truth
- replay may be hosted publicly as static evidence

### Alexa to governed work
**VERIFIED for repo/task creation**
- Ambient Guardian main `76dc8bc0...`
- signed simulator
- GitHub + Ops Task creation

Not yet proven for the new programming phrase:
- physical Echo spoken confirmation;
- final agent completion for canonical `draftd0f` task.

## Reconciled local evidence

### Local AMD benchmark
**MEASURED** from canonical `hackathon_amd_inference_benchmark.json`:
- 20 inference runs;
- p50 `0.2622 s`;
- p95 `0.2638 s`;
- throughput `22.85 tok/s`;
- Radeon AI PRO R9700, ROCm, vLLM and Qwen3-Coder AWQ.

These are latency/throughput measurements, not power-efficiency results.

### Multi-agent coordination
**VERIFIED CROSS-TEST COVERAGE** from `coordination_cross_test_report.json`:
- 6 external checks passed;
- 8 Dev Swarm lanes passed with unique nonces.

This does not establish eight simultaneously active agents.

## Scenario estimate
The 43 min / 95.56% Human Time Returned figure is a **scenario baseline estimate**.

## Public hosting
A hostname is not considered operational until an external HTTP request succeeds.

Cloudflare MCP Small is not itself proof of a public demo.

## Scope separation
- ACT III owns AMD/Gemma/Evolus/Judge Console/submission.
- Ambient Guardian owns Alexa implementation.
- InnerOps owns coordination/runtime infrastructure.
- ACT III may reference verified connected capabilities but must not duplicate their code.
