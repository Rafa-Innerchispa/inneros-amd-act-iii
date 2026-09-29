# ACT III Phase 0 Status — 2026-09-28

## Event facts verified

- Event: AMD Developer Hackathon: ACT III
- Online build: 12–18 October 2026
- On-site phase: 17–18 October 2026
- Submission deadline: 18 October 2026, 15:00 UTC
- On-site locations currently listed: Rome, Milan, Imperia
- Tracks: still TBA as of 2026-09-28
- Official page: https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-iii

## Baseline state

Canonical repository: `Rafa-Innerchispa/inneros-amd-act-iii`

Pre-ACT III baseline remains pre-hackathon work and must not be represented as newly invented during the official build window.

The AMD node checkout was reconciled to remote `main` at `abfc0b5860b1be81d177d96e994634968b65a86c` before this Phase 0 branch was created.

Baseline suite: 6/6 PASS.

## Phase 0 additions in this branch

### Execution evidence v1

Added dependency-light contracts for:

- runtime identity;
- explicit truth state: PROVEN / PARTIAL / CONTRACT-ONLY / PLANNED;
- execution identity and route reasons;
- output SHA-256;
- deterministic canonical execution hashes;
- evidence-bundle manifests;
- bundle verification.

### Human Time Returned contract

Added a strict Human Time Returned metric with:

- baseline manual seconds;
- active human seconds;
- returned seconds;
- automation rate;
- MEASURED vs ESTIMATED source state;
- fail-safe non-negative behavior.

### Truthful demo bundle

The demo now produces a machine-readable execution bundle instead of only printing routing decisions.

Current truth boundary:

- AMD local / Radeon AI PRO R9700: PROVEN as an available physical target in the wider InnerOS environment.
- AMD cloud: CONTRACT-ONLY until ACT III provides the exact cloud hardware/runtime/access.
- Demo HTR numbers: ESTIMATED, never presented as measured.

## Tests

Current suite: 11/11 PASS.

Coverage includes:

- privacy forces local;
- privacy fails closed if local is unavailable;
- elastic capacity routes cloud when available;
- local-first default;
- cloud fallback;
- routing hash verification;
- execution hash determinism;
- evidence-bundle verification;
- Human Time Returned calculation;
- non-negative HTR boundary;
- demo truth-state enforcement.

## Next technical gates

Before kickoff:

1. capture a reproducible local R9700 runtime-identity record from the physical AMD node;
2. connect the ACT III local adapter to a real InnerOS local execution lane;
3. add offline replay verification for recorded bundles;
4. add concurrency/latency benchmark output;
5. prepare the visual task-graph shell;
6. freeze the final pre-hackathon baseline SHA immediately before kickoff.

At kickoff:

1. re-read official rules/tracks;
2. select the track;
3. record exact AMD cloud hardware/runtime/access;
4. create the official ACT III implementation branch;
5. keep every new feature attributable to the frozen baseline.
