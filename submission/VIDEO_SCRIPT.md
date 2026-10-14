# Video Script — ACT III Final Story

Target length: **4:15–4:35**

Goal: tell the origin story, prove that InnerOS is broader than agent coordination, and spend most of the video showing one real Bellini flow.

---

## 0:00–0:25 — It started with one AMD GPU

I did not start by trying to build an operating system for AI agents.

I started with one AMD GPU.

After getting access to a Radeon AI PRO R9700 and ROCm, serious local AI suddenly became practical. Then AMD Skills showed another possibility: coding agents could consume validated, hardware-aware workflows directly inside tools like Cursor and Codex.

My first thought was simple:

Connect the skills, connect the agents, connect the GPU — and let them work together.

It sounded almost easy.

---

## 0:25–0:55 — The part that was not easy

The models could reason.
The GPU could run them.
The skills could teach repeatable workflows.

But capable agents did not automatically become a reliable team.

Tasks got stuck. Claims expired. Headless workers died. AMD and Intel execution behaved differently. Owner approvals duplicated. An agent could finish work while coordination still believed it was running.

Every failure exposed another missing layer.

That missing layer became InnerOS.

---

## 0:55–1:30 — What InnerOS became

InnerOS is a local-first operating fabric between human intent, interfaces, agents, compute, physical infrastructure and evidence.

Today the model is simple:

ChatGPT orchestrates.
Local AMD and Intel workers execute first.
Cursor, Codex and Antigravity become specialist lanes.
The owner is interrupted only when a decision really deserves a human.

Underneath that are the less glamorous systems that make autonomy real: task ownership, Temporal and Mongo coordination, isolated worktrees, retries, recovery, runtime registration, approval gates and fail-closed evidence.

But coordination is only one layer of InnerOS.

---

## 1:30–2:05 — Voice, buildings and the physical world

VoiceOps lets a person speak an operational intent instead of opening five tools.

InnerOS provides the context, routing, policy, approval, execution and evidence behind that voice interaction.

Physical Guardian extends the same fabric to existing cameras, DVRs, NVRs and access systems.

And Bellini I-II became our first real building operations site: networking, Wi-Fi, CCTV, recorders, intercoms, access control and voice infrastructure, all inside one environment that already existed before InnerOS arrived.

This is where the system stopped being an architecture diagram.

---

## 2:05–3:10 — Live ACT III story: Bellini

Here is the workflow we demonstrate.

The operator asks:

“Ralphi, what is happening with the cameras in Bellini?”

VoiceOps creates the intent and correlation context.

InnerOS opens the incident and delegates the work.

The Network Engineer agent loads persistent Bellini knowledge.

Guardian and Device Fabric provide asset, reachability and service evidence.

Instead of assuming that one unreachable management IP means an entire switch is down, InnerOS separates the management plane, data plane, downstream health and shared failure domain.

Local Qwen reasoning runs on AMD ROCm.

The system correlates affected services, retrieves topology and previous findings, and produces the safest remediation plan it can justify from evidence.

If that plan would change real infrastructure, InnerOS stops and requests explicit owner approval.

Then it executes — or safely simulates the action for the public demo — and verifies the result.

Bellini already gives us measurable value: a preventive technical dossier that was estimated at 240 to 300 minutes of manual work can be produced through the AI Ops workflow in roughly 30 minutes.

That is an estimated pilot saving of about 87.5 to 90 percent.

---

## 3:10–3:40 — Local-first, not local-only

InnerOS is local-first, not isolated.

Google Cloud is already part of the fabric through governed Gemini/Vertex integration, Firestore, Pub/Sub and evidence paths.

For ACT III we are also preparing Evolus as an optional business-process specialist, using its own open model through vLLM on AMD Developer Cloud — without consuming the local R9700.

These systems can extend InnerOS, but they do not become the authority.

InnerOS keeps the approval, execution and evidence boundary.

---

## 3:40–4:10 — Evidence and trust

The important part is not only that an agent produced an answer.

InnerOS records which agent acted, what skill or tool was used, where the workload ran, why that route was selected, the runtime identity, timestamps, artifacts, output hashes, approval and verification.

That execution can later be inspected and replayed.

We also track Human Time Returned, because the purpose of autonomy is not simply to make more AI calls. It is to return useful human time while preserving the decisions that should remain human.

---

## 4:10–4:30 — Closing

One AMD GPU gave us enough local intelligence to try building a team of autonomous agents.

Discovering why that was not magically enough is what created InnerOS.

AMD did not simply make InnerOS faster.

It changed what we believed could remain local, autonomous and under our control.

This is InnerOS:

from one GPU to an operating fabric for agents, voice, buildings and verifiable autonomous work.
