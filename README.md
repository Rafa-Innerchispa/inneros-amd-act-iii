# INNEROS

## Governed AI Operations on AMD

### **Reason. Act. Prove.**

**Gemma LIVE VERIFIED · Evolus LIVE VERIFIED · Evidence REPLAYABLE**

> **Companies don’t need another AI chat. They need AI that can reason, act and prove what it did.**

InnerOS is a local-first AI operations fabric that turns AMD-hosted intelligence into governed real-world action with policy, human boundaries, verification and replay.

### The ACT III proof

```text
Bellini incident
      ↓
Gemma-4-31B-IT
AMD Developer Cloud / ROCm
      ↓
structured IncidentPlan
      ↓
Evolus Workflow + Knowledge Library
      ↓
InnerOS Evidence / Replay
```

The judge can inspect a fresh live path, replay a previously verified run, or use a clearly labeled mock. Those states are intentionally different.

## Watch InnerOS resolve a real incident

Run locally:

```bash
python -m pip install -e .
python -m inneros_act3.judge_console
```

Open:

`http://127.0.0.1:8765`

### Public demo
Preferred final hostname:

`https://inneros-act3.creatorcore.ai/`

**Status: PENDING EXTERNAL HTTP VERIFICATION.**

If Cloudflare is unavailable, the project may publish a zero-cost static **LIVE VERIFIED · REPLAY** build. Static replay never pretends to execute a fresh provider call.

## Why AMD

ACT III uses **Gemma-4-31B-IT through AMD Developer Cloud / ROCm** for the verified reasoning lane.

InnerOS also has a local AMD execution lane using:
- Radeon AI PRO R9700
- vLLM
- Qwen3-Coder AWQ

Final N=20 p50 and tok/s values are published only from the canonical Intel evidence JSON. Historical benchmark numbers are intentionally excluded.

## Verified partner evidence

### Gemma
- **LIVE_VERIFIED**
- model: `Gemma-4-31B-IT`
- endpoint: `https://developer.amd.com.cn/radeon/api/v1`
- completion ID: `615398e579fb46e8be320f66c82e4b31`
- 12 available models discovered

### Evolus
- **LIVE_VERIFIED**
- MCP: `https://api.evolus.ai/mcp`
- server: Evolus2 Data Server v1.0.0
- application: InnerOS
- app ID: `80dfecd4-8474-4aad-9565-5b7a2be10ea4`
- building blocks: `workflow`, `knowledge_library`

### Evidence
Verified dual-prize bundle:

`6ee36d6905929b176fd9c49f3c1a4aa165df4a8231d5047871f581eb73b3f845`

## Voice becomes governed work

A connected InnerOS capability demonstrates a second interface:

```text
Alexa / Inner Oz
      ↓
InnerOS
      ↓
GitHub repo + governed Ops Task
      ↓
selected AI agent
      ↓
AMD local execution lane
```

Canonical voice-created demo repo:

`https://github.com/Rafa-Innerchispa/inneros-alexa-amd-draftd0f`

The GitHub repository and Ops Task creation are verified. Agent completion is not claimed until terminal evidence exists.

> **Alexa does not execute infrastructure. Alexa talks to InnerOS. InnerOS decides what is allowed to happen.**

## Governance is the product

InnerOS separates:
- reasoning;
- policy;
- approval;
- execution;
- verification;
- evidence.

Models and interfaces can change. The governance fabric remains.

## Human Time Returned

Current scenario baseline:
- manual baseline: 2700 s
- active human: 120 s
- returned: 2580 s
- automation: 95.56%

This is a **scenario baseline estimate**, not an independently measured productivity benchmark.

## Submission package

- [Final Source of Truth](submission/FINAL_SOURCE_OF_TRUTH.md)
- [Final Submission Copy](submission/SUBMISSION_FINAL.md)
- [Final Video Script](submission/VIDEO_SCRIPT_FINAL.md)
- [Pitch Deck Outline](submission/PITCH_DECK_OUTLINE.md)
- [Cover Brief](submission/COVER_BRIEF.md)
- [Final Checklist](submission/FINAL_CHECKLIST.md)
- [Truth and Scope](docs/TRUTH_AND_SCOPE.md)

## Architecture

```text
Human / Workflow / Voice
          │
          ▼
        InnerOS
Policy · Identity · Governance · Evidence
    │                    │
    ▼                    ▼
AMD intelligence      Real systems
Gemma / Qwen          GitHub / workflows
    │                    │
    └──────────┬─────────┘
               ▼
        Verify + Replay
```

## Truth labels

- **LIVE_VERIFIED**
- **VERIFIED**
- **LIVE_VERIFIED_REPLAY**
- **MOCK**
- **PENDING**
- **ENGINEERING_TRACK**

See `docs/TRUTH_AND_SCOPE.md` before changing public claims.

## License

MIT.
