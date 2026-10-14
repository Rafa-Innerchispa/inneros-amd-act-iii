# Bellini I-II — From Reactive Support to an InnerOS Building Agent

## Why Bellini matters to ACT III

Bellini I-II is the first real building site where InnerOS is being used to turn fragmented physical-infrastructure support into an observable, documented and progressively automatable operation.

The ACT III story should not present Bellini as a synthetic demo. It is a real operational environment with CCTV, access control, voice infrastructure, Wi-Fi, managed and unmanaged switching, recorders, intercoms and remote access.

## The starting point

The operational problem was intermittent degradation across cameras, recorders and related building services. The highest-value question was not “which camera is broken?” but “which shared transport/failure domain explains several devices disappearing together?”

Authorized scope:
- Bellini I-II only
- network `192.168.3.0/24`
- remote access through an authorized Tailscale subnet route
- read-only diagnostics unless the owner explicitly expands scope

Key infrastructure includes:
- Grandstream GCC6010 gateway/router
- Grandstream UCM voice core
- Grandstream GWN7801P Console managed switch
- Hikvision DS-3E1510P-EI/M Administration managed PoE switch
- multiple GWN access points
- Hikvision / Hilook / Dahua recorders and cameras
- Hikvision video-intercom / access devices
- Kantech vehicle access

The original incident included a reported failed optical path between Console and Administration and a believed copper fallback path through floor 0. InnerOS preserves an important truth boundary: fiber/SFP remains a hypothesis until physical or vendor telemetry proves it.

## The diagnostic change

The project moved away from device-by-device guessing toward failure-domain reasoning.

The canonical diagnostic model separates:
- management-plane status
- data-plane status
- service status
- downstream health
- upstream path / failure domain

A key regression lesson is the historical `.185` managed-switch case: a management IP can be unreachable while downstream forwarding continues. InnerOS therefore must not convert “management unreachable” into “device fully offline” without evidence.

## Guardian + Device Fabric

Network Guardian tracks:
- availability
- packet loss / latency
- TCP service health
- known gateway, UCM, NVR, AP and switch assets
- Tailscale state
- snapshots and incidents

Device Fabric provides:
- vendor/protocol abstraction
- discovery and inventory
- stable asset identity
- provenance
- topology reconstruction
- eventual asset graph reconciliation

The intended AG-60 flow is:

`Device Fabric -> providers -> Topology Graph -> Guardian/time-series -> Recovery Advisor -> Governed Action -> approval/Temporal -> execution -> verify/rollback/evidence`

## The Network Engineer Agent

ACT III should show Bellini as the environment that pushed AG-60 from “monitoring” toward a persistent specialist agent.

The current Network Engineer contract includes:
- observe / diagnose first
- durable site facts and findings
- persistent snapshot indexes
- Bellini cross-building segmentation policy
- governed change / verify / rollback
- disaster-recovery boundaries
- no plaintext credentials or private topology in public Git

The agent is designed to remember the building instead of re-learning the site on every incident.

## Physical Guardian

Bellini is also a target site for InnerOS Physical Guardian.

Physical Guardian is designed to reuse existing CCTV estates instead of forcing full hardware replacement:

`DVR/NVR/IP camera -> universal ingestion -> perception -> anomaly/behavior reasoning -> InnerOS policy -> bounded action -> verification -> forensic evidence`

Bellini can use a low-cost Windows/edge gateway consuming the existing camera infrastructure and initiating outbound encrypted transport, without exposing DVR/NVR devices directly to the public Internet.

## InnerOps Buildings product path

Bellini is the first real demonstrative site for:

**InnerOps Buildings — Discovery & Diagnostics, powered by InnerOS**

Current product phases:
1. Discovery & Diagnostics
2. Monitor
3. Recovery

Ready/pilotable:
- authorized site discovery
- safe read-only probes
- inventory and classification
- topology reconstruction with confidence/provenance
- observability and health
- diagnostic assistance
- technical reporting
- case documentation and metrics

Still evolving:
- fully reconciled multi-fabric asset graph
- automated failure-domain correlation end-to-end
- deeper vendor actions
- governed recovery at production scale
- autonomous corrective execution

## Measurable value

Bellini gives ACT III a business metric rather than a generic “AI saves time” claim.

Preventive technical dossier pilot:
- manual baseline estimate: 240–300 minutes
- AI Ops workflow: ~30 minutes
- estimated saving: 210–270 minutes
- estimated relative reduction: 87.5%–90%

This must be presented as an **estimated pilot saving**, not an independent controlled study.

Next metrics to instrument:
- MTTD
- time-to-diagnosis
- MTTR
- avoided field visits
- recurrence by failure domain
- percentage of critical assets monitored
- false-offline rate
- incidents correlated to a shared failure domain
- monthly operator hours saved

## ACT III demo role

Bellini is not the whole InnerOS story. It is the proof that the same operating fabric can reach the physical world.

Recommended demo arc:
1. operator asks through VoiceOps what is happening in Bellini;
2. InnerOS creates the incident context;
3. Network Engineer Agent loads persistent Bellini memory;
4. Guardian / Device Fabric provide live or captured evidence;
5. local AMD reasoning correlates the failure domain;
6. a recommendation or bounded action candidate is produced;
7. consequential actions require owner approval;
8. verification records the outcome;
9. evidence and replay preserve what happened;
10. optional Google/Evolus specialist lanes receive sanitized business/evidence events without taking control away from InnerOS.

## Truth boundary

For the public demo:
- do not expose private customer credentials;
- do not reveal sensitive internal topology beyond sanitized diagrams;
- distinguish live telemetry from captured/replayed evidence;
- do not claim fiber/SFP as proven root cause without field telemetry;
- do not claim autonomous corrective execution beyond what is actually demonstrated.

## Canonical source lineage

Primary internal sources:
- `Rafa-Innerchispa/bellini-i-ii`
- `Rafa-Innerchispa/inneros-physical-guardian`
- `Rafa-Innerchispa/innerops-agentic-platform` PR #177 (persistent Network Engineer memory)
