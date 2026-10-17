# InnerOS ACT III — Final Source of Truth

Status: **FROZEN FOR FINAL SUBMISSION**
Date: 2026-10-16
Canonical title: **InnerOS — Governed AI Operations on AMD**
Tagline: **Reason. Act. Prove.**

This file is the authoritative narrative/evidence freeze for the final ACT III submission. If another document conflicts with this file, this file wins unless a newer verified evidence artifact explicitly supersedes it.

## 1. Product thesis

**InnerOS is a local-first AI operations fabric that turns AMD-hosted intelligence into governed real-world action with policy, human boundaries, evidence, verification and replay.**

The submission must not look like a Bellini-only project. Bellini is the real-world workload used to prove the platform.

## 2. Primary ACT III proof

Bellini incident
→ **Gemma-4-31B-IT**
→ **AMD Developer Cloud / ROCm**
→ structured **IncidentPlan**
→ **Evolus Workflow + Knowledge Library**
→ **InnerOS Evidence / Replay**

### Verified partner evidence

#### Gemma
- Status: **LIVE_VERIFIED**
- Endpoint: `https://developer.amd.com.cn/radeon/api/v1`
- Model: `Gemma-4-31B-IT`
- Models discovered: **12**
- Live completion ID: `615398e579fb46e8be320f66c82e4b31`

#### Evolus
- Status: **LIVE_VERIFIED**
- MCP transport: `https://api.evolus.ai/mcp`
- Server: **Evolus2 Data Server v1.0.0**
- Application: **InnerOS**
- Application ID: `80dfecd4-8474-4aad-9565-5b7a2be10ea4`
- Verified building blocks: **workflow**, **knowledge_library**

#### Dual-prize proof
- Bundle SHA-256: `6ee36d6905929b176fd9c49f3c1a4aa165df4a8231d5047871f581eb73b3f845`
- Partner/live proof suite: **28/28 PASS**

## 3. AMD local execution proof

The public narrative may show the local AMD lane as a second proof of the broader InnerOS compute fabric.

Required exact evidence sources on Intel:

- `/home/rlopez/inneros/inneros_core/var/evidence/CHATGPT_HANDOFF_HACKATHON.md`
- `/home/rlopez/inneros/inneros_core/var/evidence/hackathon_github_summary.json`
- `/home/rlopez/inneros/inneros_core/var/evidence/hackathon_amd_inference_benchmark.json`
- `/home/rlopez/inneros/inneros_core/var/evidence/hackathon_alexa_amd_bridge.json`
- `/home/rlopez/inneros/inneros_core/var/evidence/coordination_cross_test_report.json`

Only those JSON values may be used for the final AMD performance slide:
- Radeon AI PRO R9700
- vLLM
- Qwen3-Coder AWQ
- N=20
- p50 latency
- tokens/second

**Do not substitute older HyperLoom or unrelated R9700 benchmarks.**
Canonical N=20 result: **0.2622 s p50**, **0.2638 s p95**, and **22.85 tokens/s** using `QuantTrio/Qwen3-Coder-30B-A3B-Instruct-AWQ` through vLLM/ROCm on Radeon AI PRO R9700. These are inference latency/throughput measurements, not power-efficiency results.

## 4. Alexa / Inner Oz → InnerOS → agents

This is a connected capability, not duplicated ACT III product code.

Canonical flow:

**Alexa / Inner Oz**
→ **InnerOS**
→ policy / task creation
→ public GitHub repository
→ governed Ops Task
→ selected AI agent
→ AMD local execution lane

Ambient Guardian canonical repo:
`Rafa-Innerchispa/inneros-ambient-guardian-amazon-2026`

Verified main:
`76dc8bc0dc443d092f4f37d489644346890ab53f`

Verified state:
- PR #49 merged.
- PR #50 merged.
- **188 tests PASS.**
- Signed Alexa simulator recognizes **Inner Oz**.
- Signed simulator recognizes the programming flow.
- Programming flow creates a GitHub repo + InnerOS Ops Task.
- `voice_program_dispatch` remains opt-in.
- Default `DRAFT_ONLY` safety boundary is preserved.

Canonical voice-created demo repo for the presentation:
`https://github.com/Rafa-Innerchispa/inneros-alexa-amd-draftd0f`

Associated Ops Task:
`ops_341ecfcc1e0d`

Truth boundary:
- **VERIFIED:** voice request → GitHub repo + Ops Task.
- **PENDING:** physical Echo spoken confirmation for the new programming phrase.
- **PENDING:** Antigravity completion of the `draftd0f` programming task unless terminal evidence proves otherwise.

Do not present `draftb2b`, `draft600`, or `draftc6b` as the canonical demo repository. They are test artifacts.

## 5. Existing physical / governed voice capability

Ambient Guardian has separate existing evidence for:
- real energy/status queries;
- governed UniFi action with approval boundary;
- Alexa as the natural-language entry point to InnerOS.

For the ACT III story, use Alexa to prove **interface-to-governed-work**, not to turn ACT III into an Alexa hackathon entry.

Core sentence:

> **Alexa does not execute infrastructure. Alexa talks to InnerOS. InnerOS decides what is allowed to happen.**

## 6. Public demo requirement

The final submission requires a real Application URL.

### Preferred
Publish Judge Console / Verified Replay through an existing authorized Cloudflare path.

Preferred hostname:
`https://inneros-act3.creatorcore.ai/`

Another owner-approved hostname under an existing zone is acceptable if the preferred name conflicts.

A public URL is **VERIFIED only after external HTTP 200 succeeds**.

Verified zero-cost fallback (external HTTP 200 on October 16, 2026):
`https://rafa-innerchispa.github.io/inneros-amd-act-iii/`

### Current Cloudflare infrastructure truth
- MCP Small Cloudflare capability is **not currently available**.
- Existing repair task: `ops_4fe9cc3d9390`
- Existing repair PR: innerops-agentic-platform **#186**
- Do not block final submission waiting for that platform repair.
- Codex may use an already authenticated safe `cloudflared`/Cloudflare path if available.
- No unrelated DNS/WAF mutations.
- No secrets in repo/logs.

### Fallback
If Cloudflare is genuinely blocked, publish the static Judge Console / **Verified Replay** through GitHub Pages or another existing zero-cost public path in the same repo.

Hosted static mode must never claim fresh LIVE execution.

## 7. Judge Console first screen

The first screen must communicate the platform in under 15 seconds:

# INNEROS
## Governed AI Operations on AMD
### Reason. Act. Prove.

Status pills:
- **Gemma LIVE VERIFIED**
- **Evolus LIVE VERIFIED**
- **Evidence REPLAYABLE**

Capability spine:
**AMD Developer Cloud / ROCm → Gemma reasoning → Evolus business workflow → InnerOS evidence**

CTA:
**Watch InnerOS resolve a real incident**

Then transition into:
**Bellini → Gemma → Evolus → Evidence**

Controls to preserve:
- Run Live Demo
- Replay Verified Run
- Mock
- fail-closed truth labels
- IncidentPlan
- Evolus Work Order
- SHA-256 evidence receipt

## 8. Pitch deck freeze

Maximum 8 slides.

1. **InnerOS — Governed AI Operations on AMD**
   - Reason. Act. Prove.
2. **The problem**
   - AI can reason. Businesses need governed action and proof.
3. **AMD engine**
   - Radeon AI PRO R9700 / vLLM / Qwen3-Coder AWQ
   - use exact N=20 p50 and tok/s from Intel JSON only.
4. **ACT III proof**
   - Bellini → Gemma on AMD → Evolus → Evidence.
5. **Voice-to-work**
   - Alexa / Inner Oz → InnerOS → GitHub + agents → AMD.
6. **Governance**
   - policy, human boundary, fail-closed behavior, evidence, replay.
7. **Business value**
   - Human Time Returned may be shown only as a **scenario baseline estimate**.
8. **Close**
   - InnerOS makes AI operational, accountable and deployable.

## 9. Video freeze

Target: 90–120 seconds.

Opening line:

> **Companies don’t need another AI chat. They need AI that can reason, act and prove what it did.**

Sequence:
1. InnerOS thesis.
2. AMD compute / Gemma.
3. Bellini incident.
4. structured IncidentPlan.
5. Evolus workflow/work order.
6. InnerOS evidence receipt/replay.
7. Alexa/Inner Oz as a second natural-language entry point to governed work.
8. close: **Reason. Act. Prove.**

## 10. Human Time Returned

Existing values:
- manual baseline: 2700 s
- active human: 120 s
- returned: 2580 s
- automation rate: 95.56%

Allowed wording:
**Scenario baseline estimate: 43 minutes returned / 95.56% automation.**

Forbidden wording:
- independent measured productivity benchmark;
- scientifically measured HTR;
- universal 95.56% productivity improvement.

## 11. Multi-agent concurrency

Do not claim 4 or 8 simultaneously active agents as a final demonstrated ACT III fact unless the exact `coordination_cross_test_report.json` proves that claim and the final submission text cites that evidence faithfully.

Allowed:
**Multi-agent coordination cross-test — VERIFIED: 6 external checks and 8 Dev Swarm lanes with unique nonces.** This is coverage evidence, not proof of eight simultaneously active agents.

Forbidden without exact proof:
- “8 agents running simultaneously”
- “4-agent live swarm”
- “verified 8-lane autonomy”

## 12. Claim control table

| Claim | Status | Evidence | Allowed wording | Forbidden wording |
|---|---|---|---|---|
| Gemma on AMD Developer Cloud | LIVE_VERIFIED | completion ID + live tests | Gemma LIVE VERIFIED | mock-only / local R9700 Gemma |
| Evolus MCP integration | LIVE_VERIFIED | server/app/building blocks | Evolus LIVE VERIFIED | simulated Evolus |
| Evidence replay | VERIFIED | bundle SHA + replay fixture | Evidence REPLAYABLE | fresh LIVE when static |
| Bellini incident lane | VERIFIED DEMO LANE | ACT III repo evidence | real-world Bellini scenario | uncontrolled production mutation |
| Alexa creates repo + Ops Task | VERIFIED | Ambient Guardian main + signed simulator | Voice-to-governed-work verified | agent finished code unless terminal |
| New programming phrase on physical Echo | PENDING | owner spoken confirmation required | pending physical confirmation | LIVE_VERIFIED today |
| Local AMD R9700 benchmark | MEASURED | Intel benchmark JSON | N=20 p50 0.2622 s; p95 0.2638 s; 22.85 tok/s | old/derived or efficiency values |
| HTR 43 min / 95.56% | SCENARIO BASELINE | dual-prize scenario | scenario baseline estimate | measured productivity fact |
| 4/8 simultaneous agents | ENGINEERING TRACK unless JSON proves | cross-test JSON | architecture / engineering track | verified live swarm without proof |
| Public demo | LIVE VERIFIED · REPLAY | GitHub Pages workflow + external HTTP 200 | https://rafa-innerchispa.github.io/inneros-amd-act-iii/ | fresh LIVE execution |

## 13. Repository storage map

These files form the final submission package:

- `submission/FINAL_SOURCE_OF_TRUTH.md` — this file, canonical freeze.
- `submission/SUBMISSION_FINAL.md`
- `submission/VIDEO_SCRIPT_FINAL.md`
- `submission/PITCH_DECK_OUTLINE.md`
- `submission/COVER_BRIEF.md`
- `submission/FINAL_CHECKLIST.md`
- `docs/TRUTH_AND_SCOPE.md`
- `README.md`
- `docs/demo/` static Verified Replay when used.

## 14. Build lineage / originality boundary

The submission must explicitly distinguish three categories:

### Pre-existing before ACT III
- InnerOS control plane and governance.
- MCP/A2A and local execution plane.
- local AMD ROCm/vLLM/Qwen execution.
- evidence/replay design.
- Human Time Returned design.
- Bellini as an existing real-world operational context.

### Built or integrated during ACT III
- AMD Developer Cloud + Gemma live integration.
- structured IncidentPlan contract.
- Evolus MCP + Workflow + Knowledge Library integration.
- Bellini → Gemma → Evolus → Evidence end-to-end partner pipeline.
- ACT III-specific evidence bundle and partner verification.
- Judge Console.
- container/static/public demo packaging.
- final submission/video/deck/cover/truth package.

### Reused from the parallel Alexa hackathon
- Inner Oz / Alexa interface.
- real energy/status queries.
- governed physical-action pattern.
- voice → GitHub repo + InnerOS Ops Task programming dispatch.

ACT III references that Alexa capability as proof that InnerOS is reusable across interfaces; it does not claim the Alexa implementation was created entirely inside ACT III.

Full lineage:
`docs/ACT3_BUILD_LINEAGE.md`

## 15. Final success criteria

Submission is ready only when:
- all submission docs are consistent with this file;
- exact Intel benchmark values are inserted from the JSON evidence;
- tests pass;
- no secrets are present;
- README first screen is judge-ready;
- public Application URL returns external HTTP 200;
- static/public replay has honest truth labels;
- final branch/SHA/PR are recorded;
- no unsupported claim remains.

**Winning principle: show more proof than promises.**
