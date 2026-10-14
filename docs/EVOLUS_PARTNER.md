# Evolus Business Agents — ACT III Partner Track Specification

## Overview

In the **AMD Developer Hackathon ACT III**, InnerOS integrates **Evolus Business Agents** as the governed **business operations layer** for autonomous infrastructure and smart-building incident management (Bellini Tower showcase).

Evolus acts as the domain business workflow and knowledge engine. It does **not** replace the InnerOS sovereign control plane or execution boundary:
1. **InnerOS** detects and sanitizes infrastructure telemetry.
2. **Gemma (AMD Token Factory)** formulates a structured `IncidentPlan`.
3. **Evolus** applies domain policies, standard operating procedures (SOPs), and automated work-order generation across two distinct building blocks.
4. **InnerOS** validates approvals, enforces local-first constraints, captures immutable SHA-256 evidence, and measures **Human Time Returned**.

---

## Evolus Hackathon Partner Compliance

| Partner Rule | InnerOS Implementation | Verification Status |
| :--- | :--- | :---: |
| **Open Model on AMD Cloud** | Evolus agent connects to our OpenAI-compatible endpoint hosting open model on AMD Developer Cloud (`https://developer.amd.com.cn/radeon/api/v1` or private vLLM). | **YES** |
| **At Least 2 Building Blocks** | Employs both **Building Block 1: Knowledge Library** (`kl-building-ops-sop`) and **Building Block 2: Workflow** (`wf-bellini-remediation`). | **YES** |
| **Driven by API** | Fully automated via REST adapter `inneros_act3.evolus_adapter` without human UI intervention. | **YES** |
| **No Secrets in Git** | All keys resolved strictly via environment variables (`EVOLUS_API_KEY`) or encrypted server vault (`owner_vault:evolus/api_key`). | **YES** |
| **Zero Paid External Inference** | Models run on AMD Developer Cloud / ROCm endpoints. | **YES** |

---

## Architecture & Data Flow

```mermaid
sequenceDiagram
    autonumber
    participant Sensor as Bellini Network / Guardian
    participant InnerOS as InnerOS Sovereign Core
    participant Gemma as Gemma (AMD Developer Cloud)
    participant Evolus as Evolus Business Agents
    participant Vault as Owner Vault / Evidence

    Sensor->>InnerOS: Optical link flap & telemetry alarm
    InnerOS->>Gemma: Multimodal Incident Context
    Gemma-->>InnerOS: Validated IncidentPlan (Severity: Critical)
    InnerOS->>Evolus: Query Knowledge Library (Remediation SOP)
    Evolus-->>InnerOS: Relevant SOPs (Carrier Flap, SLA Ticket)
    InnerOS->>Evolus: Trigger Workflow (IncidentPlan + SOPs)
    Evolus-->>InnerOS: Structured EvolusWorkOrder (Steps, Roles, Gates)
    InnerOS->>Vault: Emit ExecutionEvidence + Human Time Returned
```

---

## Configuration & Environment Variables

| Variable | Description | Default / Example |
| :--- | :--- | :--- |
| `EVOLUS_API_BASE` | Base URL of Evolus REST API | `https://api.evolus.ai/v1` |
| `EVOLUS_API_KEY` | Secret bearer API key | Resolved from env or `owner_vault:evolus/api_key` |
| `EVOLUS_WORKSPACE_ID` | Identifier of the hackathon workspace | `ws-act3-smartbuilding` |
| `EVOLUS_WORKFLOW_ID` | Identifier of the remediation workflow | `wf-bellini-remediation` |
| `EVOLUS_KNOWLEDGE_LIBRARY_ID` | Identifier of the operational knowledge library | `kl-building-ops-sop` |
| `EVOLUS_MODEL_ENDPOINT` | Open model endpoint hosted on AMD Developer Cloud | `https://developer.amd.com.cn/radeon/api/v1` |

---

## Live Smoke & Verification Commands

### Automated Mock Verification (Offline & CI):
```bash
python -m inneros_act3.smoke --evolus --json
```

### Live Gated Preflight Verification:
```bash
python -m inneros_act3.smoke --evolus --live
```

If the API key is unconfigured in the server vault or environment, the live runner safely exits with a deterministic blocker report without crashing:
```json
{
  "track": "evolus_act3_partner",
  "status": "BLOCKED",
  "eligibility": "NO_CREDENTIAL_BLOCKED",
  "required_env_vars": ["EVOLUS_API_KEY", "EVOLUS_WORKSPACE_ID", "EVOLUS_WORKFLOW_ID", "EVOLUS_KNOWLEDGE_LIBRARY_ID"]
}
```

---

## Eligibility Verdict

- **Evolus Business Agents Track Eligibility:** **YES**
