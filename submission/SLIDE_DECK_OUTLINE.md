# ACT III Slide Deck — 16-slide Story + Product Structure

## Slide 1 — From One AMD GPU to InnerOS
Title:
**InnerOS: From One AMD GPU to Autonomous Ops**

Subtitle:
A local-first operating fabric for agents, voice, buildings, cloud and verifiable autonomous work.

Message:
The hardware changed the architecture of the product.

---

## Slide 2 — The idea that sounded easy
**AMD ROCm + AMD Skills + coding agents + local models = autonomous team?**

Show:
- Radeon AI PRO R9700
- ROCm
- AMD Skills
- Cursor
- Codex
- Antigravity
- local Qwen/vLLM

Close:
**The pieces worked. The system did not exist yet.**

---

## Slide 3 — What broke first
Visual: failure chain / incident timeline.

- tasks stuck between queues
- claims/leases expired
- headless workers died
- false completion without evidence
- AMD/Intel asymmetry
- repositories not safely executable
- external-agent ownership collisions
- duplicate owner authorization

Message:
**Capable agents are not automatically a reliable operating system.**

---

## Slide 4 — InnerOS emerges
Architecture layers:

Human intent / Voice / Web / WhatsApp
↓
InnerOS control plane
↓
Coordination + routing + policy + approvals
↓
Agents + skills + tools
↓
AMD / Intel / approved cloud
↓
Physical systems + software systems
↓
Evidence + replay

Callouts:
- Temporal + Mongo
- Project Runtime Registry
- worktrees
- bounded execution
- retries/recovery
- fail-closed evidence

---

## Slide 5 — The compute fabric
Show three compute zones:

### Local AMD
- Radeon AI PRO R9700
- ROCm
- vLLM / Qwen
- private / latency-sensitive reasoning

### Local Intel
- Ollama / local fallback
- second execution node

### Cloud extensions
- AMD Developer Cloud
- Google Cloud strategic lane

Message:
**Local-first, not local-only.**

---

## Slide 6 — The agent operating model
Show live operating model:

**ChatGPT orchestrates**
→ **Dev Swarm AMD + Intel executes first**
→ **Cursor / Codex / Antigravity specialist lanes**
→ **WhatsApp only for real owner decisions**

Representative agents:
- AG-60 Network Engineer
- Bellini building agent
- VoiceOps
- AG-44 Cloud Deployer
- GitHub/GitLab development lanes
- Physical Guardian

Message:
Agents are specialized and bounded, not omnipotent.

---

## Slide 7 — VoiceOps: speech becomes governed action
Flow:

Human voice
→ realtime speech understanding
→ InnerOS Voice Gateway
→ context / policy
→ local AMD reasoning
→ capability / MCP
→ approval
→ PBX / operational action
→ evidence + replay

Message:
**Voice is the interface. Governed execution is the product.**

---

## Slide 8 — Bellini: where InnerOS met the physical world
Title:
**A real building, not a synthetic benchmark**

Show sanitized building topology:
- GCC6010 gateway
- UCM voice core
- managed + unmanaged switching
- GWN Wi-Fi
- CCTV/NVR
- video intercom / access control
- Tailscale remote path

Problem:
intermittent multi-service degradation.

Message:
We stopped asking “which camera failed?” and started asking “which shared failure domain explains the incident?”

---

## Slide 9 — From troubleshooting to a persistent Network Engineer
Evolution:

Reactive support
→ canonical inventory
→ Network Guardian
→ Device Fabric
→ topology/provenance
→ AG-60 Network Engineer
→ persistent site memory
→ governed change / verify / rollback

Critical lesson:
management-plane failure is not automatically data-plane failure.

Message:
The agent should remember the building instead of relearning it every incident.

---

## Slide 10 — Bellini business value
Product surface:
**InnerOps Buildings — Discovery & Diagnostics**

Roadmap:
1. Discovery & Diagnostics
2. Monitor
3. Recovery

Pilot metric:
- manual dossier: 240–300 min
- AI Ops workflow: ~30 min
- estimated saving: 210–270 min
- estimated reduction: 87.5%–90%

Label clearly:
**Estimated pilot saving, not an independent controlled study.**

---

## Slide 11 — Physical Guardian
Flow:

DVR/NVR/IP camera
→ universal ingestion
→ perception
→ anomaly/behavior reasoning
→ InnerOS policy
→ bounded action
→ verification
→ forensic evidence

Show:
- legacy analog through DVR streams
- IP cameras via RTSP/ONVIF/vendor adapters
- local/edge inference
- no need to replace the whole camera estate

---

## Slide 12 — Google is already inside the fabric
Existing components:
- Gemini / Vertex provider adapter
- Firestore evidence + memory
- Pub/Sub event path
- Model Armor
- Google ADK / A2A contract
- AG-44 cloud operations / GCP auth and planning

Truth boundary:
ADK/Gemini partner path must be shown live before being claimed as fully operational.

Message:
Google extends InnerOS; it does not replace the local-first control plane.

---

## Slide 13 — Evolus: business-process specialist on AMD cloud
Architecture:

InnerOS incident
→ Evolus Workflow
→ Knowledge Library
→ open model via vLLM on AMD Developer Cloud
→ structured work order / escalation
→ result back to InnerOS
→ owner approval / evidence

Key point:
**No second model needs to consume the local R9700.**

Partner requirement callout:
- event workspace
- own AMD vLLM endpoint
- 2+ Evolus building blocks
- API-driven integration

---

## Slide 14 — Trust: evidence, approval and replay
Show one execution receipt:
- correlation ID
- agent
- skill/tool
- route reason
- runtime identity
- timestamp
- approval
- artifact/output hash
- verification
- Human Time Returned

Message:
**Autonomy without evidence is just a demo.**

---

## Slide 15 — ACT III end-to-end demo
One continuous flow:

1. Operator asks by voice about Bellini.
2. VoiceOps creates intent/context.
3. InnerOS coordinates tasks.
4. Network Engineer loads persistent Bellini memory.
5. Guardian + Device Fabric provide evidence.
6. Local AMD ROCm performs reasoning.
7. Optional specialist agent handles bounded unsupported work.
8. Optional Google/Evolus path receives sanitized event/business context.
9. Owner approves consequential action.
10. Action executes or is safely simulated.
11. Verification confirms result.
12. Evidence + replay close the loop.
13. Human Time Returned quantifies value.

---

## Slide 16 — What AMD really enabled
Three stages:

1. **Compute** — local inference became practical.
2. **Skills** — hardware-aware workflows became agent-readable.
3. **InnerOS** — the missing operating layer turned those capabilities into governed autonomous work.

Closing line:

**One AMD GPU gave us enough local intelligence to try building a team of autonomous agents. Discovering why that was not magically enough is what created InnerOS.**

Final subtitle:
**From one GPU to an operating fabric for agents, voice, buildings and verifiable autonomous work.**
