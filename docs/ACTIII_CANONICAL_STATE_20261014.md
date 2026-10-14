# ACT III Canonical State — Gemma & Evolus Dual Partner Integration

**Date:** 2026-10-14  
**Worktree:** `antigravity__act3-gemma-evolus-20261014`  
**Host:** `ralfiia-amd` (`192.168.1.5`)  
**Linked Task:** `ops_b4c988b85337` (Revision 9)  

---

## 1. Executive Summary & Prize Eligibility

| Partner Track | Model / Component | Backend / Host | 2+ Blocks / API | Eligibility Status |
| :--- | :--- | :--- | :---: | :---: |
| **Google DeepMind Gemma Track** | `Gemma-4-31B-IT` | AMD Developer Cloud Token Factory (ROCm) | Multimodal Incident Director API | **YES** |
| **Evolus Business Agents Track** | Workflow + Knowledge Library | Open Model on AMD Cloud (`Gemma-4-31B-IT`) | REST API driven from repo | **YES** |

---

## 2. Dual-Prize Unified Architecture

```
                       [ Smart Building Incident ]
                       (Bellini Optical Flap / Alarms)
                                    │
                                    ▼
                    ┌───────────────────────────────┐
                    │  InnerOS Sovereign Core       │
                    │  (Sanitization & Telemetry)   │
                    └───────────────┬───────────────┘
                                    │
                         (1) Context Payload
                                    │
                                    ▼
       ┌────────────────────────────────────────────────────────┐
       │ Google Gemma (AMD Developer Cloud Token Factory)       │
       │ Role: Multimodal Incident Director (ROCm)              │
       │ Output: Structured, Verified IncidentPlan               │
       └────────────────────────────┬───────────────────────────┘
                                    │
                         (2) Validated Plan
                                    │
                                    ▼
       ┌────────────────────────────────────────────────────────┐
       │ Evolus Business Agents Layer                           │
       │ Block 1: Knowledge Library (SOPs & Building Policy)     │
       │ Block 2: Workflow Engine (Work Order & Remediation)    │
       │ Open Model Endpoint: AMD Developer Cloud (Gemma/ROCm)  │
       └────────────────────────────┬───────────────────────────┘
                                    │
                         (3) Structured Work Order
                                    │
                                    ▼
                    ┌───────────────────────────────┐
                    │  InnerOS Audit & Evidence     │
                    │  - SHA-256 Evidence Manifest  │
                    │  - Human Time Returned Metric │
                    │  - Local-first Governance     │
                    └───────────────────────────────┘
```

---

## 3. Test & Verification Results

All unit and integration tests execute cleanly with zero secrets leaked and zero paid external spend:

```text
============================= test session starts ==============================
collected 27 items

tests/test_core.py::RouterTests::test_cloud_fallback PASSED              [  3%]
tests/test_core.py::RouterTests::test_elastic_capacity_prefers_cloud PASSED [  7%]
tests/test_core.py::RouterTests::test_evidence_hash_verifies PASSED      [ 11%]
tests/test_core.py::RouterTests::test_local_first_default PASSED         [ 14%]
tests/test_core.py::RouterTests::test_privacy_fails_closed PASSED        [ 18%]
tests/test_core.py::RouterTests::test_privacy_forces_local PASSED        [ 22%]
tests/test_core.py::ExecutionEvidenceTests::test_bundle_manifest_verifies PASSED [ 25%]
tests/test_core.py::ExecutionEvidenceTests::test_execution_hash_is_deterministic PASSED [ 29%]
tests/test_core.py::ExecutionEvidenceTests::test_human_time_never_goes_negative PASSED [ 33%]
tests/test_core.py::ExecutionEvidenceTests::test_human_time_returned PASSED [ 37%]
tests/test_core.py::DemoBundleTests::test_demo_bundle_is_verifiable_and_truthful PASSED [ 40%]
tests/test_dual_prize.py::DualPrizePipelineTests::test_run_dual_prize_pipeline_mock PASSED [ 44%]
tests/test_dual_prize.py::DualPrizePipelineTests::test_smoke_cli_runner_all_mock PASSED [ 48%]
tests/test_dual_prize.py::DualPrizePipelineTests::test_smoke_cli_runner_individual_flags PASSED [ 51%]
tests/test_evolus_adapter.py::EvolusAdapterTests::test_evolus_smoke_live_blocked_when_no_key PASSED [ 55%]
tests/test_evolus_adapter.py::EvolusAdapterTests::test_evolus_smoke_mock PASSED [ 59%]
tests/test_evolus_adapter.py::EvolusAdapterTests::test_execute_workflow_mock PASSED [ 62%]
tests/test_evolus_adapter.py::EvolusAdapterTests::test_query_knowledge_library_mock PASSED [ 66%]
tests/test_evolus_adapter.py::EvolusAdapterTests::test_work_order_hash_is_deterministic PASSED [ 70%]
tests/test_manifest.py::test_manifest_is_local_first_and_auditable PASSED [ 74%]
tests/test_token_factory_provider.py::TokenFactoryProviderTests::test_generate_incident_plan_mock PASSED [ 77%]
tests/test_token_factory_provider.py::TokenFactoryProviderTests::test_list_models_mock PASSED [ 81%]
tests/test_token_factory_provider.py::TokenFactoryProviderTests::test_plan_hash_is_deterministic PASSED [ 85%]
tests/test_token_factory_provider.py::TokenFactoryProviderTests::test_token_factory_safety_toggle PASSED [ 88%]
tests/test_token_factory_provider.py::TokenFactoryProviderTests::test_token_factory_smoke_live_blocked_when_no_key PASSED [ 92%]
tests/test_token_factory_provider.py::TokenFactoryProviderTests::test_token_factory_smoke_mock PASSED [ 96%]
tests/test_token_factory_provider.py::TokenFactoryProviderTests::test_validate_plan_rejects_missing_fields PASSED [100%]

============================== 27 passed in 0.31s ==============================
```

---

## 4. Live Verification & Environment Requirements

For live API calls against AMD Token Factory and Evolus cloud, set the following environment variables (or insert into `owner_vault`):

```bash
# AMD Token Factory (Gemma)
export AMD_TOKEN_FACTORY_API_KEY="<your-token-factory-key>"
export AMD_TOKEN_FACTORY_BASE_URL="https://developer.amd.com.cn/radeon/api/v1"
export AMD_TOKEN_FACTORY_MODEL="Gemma-4-31B-IT"

# Evolus Partner Track
export EVOLUS_API_KEY="<your-evolus-api-key>"
export EVOLUS_API_BASE="https://api.evolus.ai/v1"
export EVOLUS_WORKSPACE_ID="<your-workspace-id>"
export EVOLUS_WORKFLOW_ID="<your-workflow-id>"
export EVOLUS_KNOWLEDGE_LIBRARY_ID="<your-knowledge-library-id>"
export EVOLUS_MODEL_ENDPOINT="https://developer.amd.com.cn/radeon/api/v1"
```

To run preflight smoke verification:
```bash
# Offline/mock verification:
python -m inneros_act3.smoke --all

# Live external verification:
python -m inneros_act3.smoke --all --live
```
