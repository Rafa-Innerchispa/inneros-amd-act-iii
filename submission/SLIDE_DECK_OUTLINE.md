# ACT III Slide Deck — Story-first Structure

## Slide 1 — It started with one AMD GPU
Title:
**From One AMD GPU to InnerOS**

Subtitle:
How local ROCm compute turned an experiment with AI agents into a sovereign execution fabric.

Visual:
Radeon AI PRO R9700 → ROCm → agents → InnerOS.

Message:
The hardware changed the architecture of the product.

## Slide 2 — The idea that sounded easy
**AMD Skills + Cursor + Codex + local inference = autonomous team?**

Show:
- AMD Skills / ROCm.AI
- Cursor
- Codex
- Antigravity
- local Qwen

Then one line:
**Not quite.**

## Slide 3 — What broke
Show the failure chain:
- task created, never claimed;
- expired lease;
- stale headless PID;
- duplicate authorization;
- incomplete evidence;
- AMD/Intel asymmetry;
- repository not registered;
- external agent ownership collision.

Message:
The agents were capable. The execution system was missing.

## Slide 4 — InnerOS emerges
Architecture:
Human / ChatGPT → InnerOS control plane → agents + skills → AMD/Intel local first → specialist external lanes.

Platform callouts:
- durable coordination
- bounded execution
- worktrees
- owner approval
- fail-closed evidence
- retries / recovery
- replay

## Slide 5 — ACT III: Intelligent Industry
Use case:
Smart-building camera/intercom degradation.

Workflow:
incident → telemetry → knowledge → plan → approval → action → verification.

Highlight local AMD ROCm route.

## Slide 6 — Evidence, not magic
Show:
- route reason
- AMD runtime identity
- agent/skill
- SHA-256 output
- elapsed time
- Human Time Returned
- replay

Message:
Autonomy without evidence is just a demo.

## Slide 7 — What AMD enabled
Three layers:
1. **Compute:** local inference became practical.
2. **Skills:** hardware-aware workflows became agent-readable.
3. **InnerOS:** coordination made those capabilities operational.

Close:
**A single AMD GPU gave us enough local intelligence to try building a team of autonomous agents. Discovering why that was not magically enough is what created InnerOS.**
