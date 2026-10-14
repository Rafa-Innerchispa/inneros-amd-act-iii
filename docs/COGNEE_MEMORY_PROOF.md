# ACT III Cognee Shared Memory Proof

## Purpose

ACT III reuses the existing InnerOS Personal Brain Cognee memory fabric instead
of inventing a second memory system.

Canonical source implementation:

- `Rafa-Innerchispa/inneros-personal-brain/app/cognee_agent_tools.py`
- `Rafa-Innerchispa/inneros-personal-brain/app/cognee_mcp_proxy.py`
- canonical dataset: `inneros-personal-brain`

This adapter proves one product claim:

> **Agent A learns -> Agent B remembers.**

## ACT III flow

A judge-safe Bellini example is:

1. AG-60 verifies a non-secret operational fact.
2. InnerOS explicitly marks that fact as safe to share.
3. `CogneeSharedMemory.remember_verified_fact()` writes the curated envelope
   to the canonical Cognee dataset.
4. Another agent, such as the Gemma Multimodal Incident Director, performs a
   recall against that same dataset.
5. ACT III emits a proof receipt with the writer agent, reader agent, dataset,
   fact hash and recall count.

The proof does **not** imply that private Bellini configuration, credentials or
raw customer payloads are copied to Cognee.

## Privacy boundary

Private operational memory remains in InnerOS private stores such as
Mongo/Qdrant.

Cognee receives only facts that satisfy both gates:

- `verified=True`
- `safe_to_share=True`

The adapter also rejects obvious sensitive metadata keys such as passwords,
tokens, credentials, API keys and PINs.

## Runtime configuration

```text
COGNEE_SERVICE_URL=https://api.cognee.ai
COGNEE_API_KEY=<server-side only>
COGNEE_DATASET=inneros-personal-brain
```

The HTTP contract matches the existing Personal Brain implementation:

- `POST /api/v1/remember`
- `POST /api/v1/recall`
- `X-Api-Key` authentication

No credential is stored in this repository.

## Truth states

- `PROVEN`: a remember call succeeded and another agent received at least one
  recalled memory in the same proof run.
- `LIVE-PARTIAL`: the write succeeded but no recall evidence was returned.
- configuration without a credential fails closed and must never be presented
  as a live proof.

## Test

```bash
python -m unittest tests.test_cognee_memory
```

The unit test uses a fake transport and does not consume Cognee credits or
require a secret.
