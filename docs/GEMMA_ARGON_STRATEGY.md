# Google Gemma on AMD Developer Cloud (ROCm) — Strategy & Architecture

## Overview

For the **Google DeepMind Gemma Track** within the **AMD Developer Hackathon ACT III**, InnerOS deploys **Gemma-4-31B-IT** on AMD GPUs via the **AMD Developer Cloud Token Factory** endpoint (`https://developer.amd.com.cn/radeon/api/v1`).

Gemma serves as the **Multimodal Incident Director**:
- Evaluates multi-source telemetry, syslog dumps, and network metrics from physical/smart-building deployments (Bellini Tower).
- Produces strongly-typed, verifiable JSON conforming to the `IncidentPlan` schema.
- Routes actions across the sovereign control plane: local ROCm execution, Evolus business workflow delegation, or human sign-off gates.

---

## Technical Specifications

| Parameter | Value |
| :--- | :--- |
| **Model** | `Gemma-4-31B-IT` |
| **Hardware Backend** | AMD GPUs in Cloud / ROCm (AMD Developer Cloud / Token Factory) |
| **Interface** | OpenAI-Compatible REST (`GET /models`, `POST /chat/completions`) |
| **Base URL** | `https://developer.amd.com.cn/radeon/api/v1` |
| **Credential Path** | `AMD_TOKEN_FACTORY_API_KEY` or `owner_vault:amd_token_factory/api_key` |
| **Rate Limit / Quota** | ~1 pt/day, 20 RPM (Daily reset at 11:00 Asia/Shanghai) |
| **Production Boundary** | Concurrency = 1, compact prompts, max 1–2 live calls/day, offline mock for CI |

---

## Schema Contract: `IncidentPlan`

All outputs from Gemma are validated against the immutable schema contract:
```json
{
  "incident_id": "INC-BELLINI-20261014-01",
  "severity": "critical",
  "category": "network",
  "diagnosis": "Loss of carrier on optical trunk interface; automated failover recommended.",
  "recommended_actions": [
    {
      "action_id": "act-1",
      "description": "Isolate flapping VLAN and transition routing to redundant gateway.",
      "reversible": true,
      "target_system": "edge_switch_01",
      "priority": "p0"
    },
    {
      "action_id": "act-2",
      "description": "Trigger Evolus business workflow for vendor escalation and dispatch.",
      "reversible": false,
      "target_system": "evolus_business_flow",
      "priority": "p1"
    }
  ],
  "delegation_lane": "evolus_business_flow",
  "model": "Gemma-4-31B-IT",
  "provider": "amd-developer-cloud-gemma",
  "raw_response_sha256": "4b92...",
  "latency_ms": 124.5,
  "tokens_used": 348
}
```

---

## Post-Hackathon Deactivation

To prevent unwanted external outbound traffic after the hackathon without mutating core platform files:
```bash
# Set in environment:
export INNEROS_ACT3_TOKEN_FACTORY_ENABLED=0
```
When set to `0` or `false`, `is_token_factory_enabled()` returns `False` and cleanly rejects external calls with `token_factory_disabled_by_env`, preserving vault keys and local capabilities.

---

## Verification Commands

### Automated Mock Verification:
```bash
python -m inneros_act3.smoke --gemma --json
```

### Live Gated Preflight Verification:
```bash
python -m inneros_act3.smoke --gemma --live
```

---

## Eligibility Verdict

- **Google DeepMind Gemma Prize Eligibility:** **YES**
