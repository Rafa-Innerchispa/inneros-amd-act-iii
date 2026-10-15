# InnerOS ACT III Judge Console

The Judge Console is the judge-facing visual surface for the ACT III live pipeline.

## Story

Bellini incident → Gemma on AMD Token Factory → Evolus Workflow + Knowledge Library → InnerOS Evidence.

This is deliberately not a chatbot. The interface shows operational reasoning, business workflow execution, truth labels, and replayable evidence.

## Run

From the repository root:

    python -m pip install -e .
    python -m inneros_act3.judge_console

Open:

    http://127.0.0.1:8765

Optional network bind:

    python -m inneros_act3.judge_console --host=0.0.0.0 --port=8765

The installed console shortcut is:

    act3-judge

## Demo modes

### Run Live Demo

The server checks live AMD Token Factory model discovery and live Evolus MCP telemetry before the UI may display LIVE VERIFIED. If either provider cannot be proven, the console fails closed to BLOCKED.

### Replay Verified Run

Loads the sanitized ACT III receipt captured during live verification. The UI displays LIVE VERIFIED · REPLAY so a judge can inspect a deterministic result without consuming another provider call.

### Mock / Offline

Runs the existing deterministic mock pipeline. The page visibly switches to MOCK MODE.

## Visual language

Red represents the incident. Electric blue represents Gemma reasoning on AMD. Cyan represents Evolus workflow/data movement. Green is reserved for cryptographically verified evidence. The animated backdrop is an abstract compute fabric rendered in canvas/CSS rather than fake hardware photography.

## Truth boundary

No API keys, bearer tokens, vault secrets, or authentication headers are sent to the browser. LIVE VERIFIED is reserved for proven live dependencies plus a verified InnerOS evidence bundle.
