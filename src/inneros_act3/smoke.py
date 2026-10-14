"""CLI smoke runner for AMD Hackathon ACT III partner tracks.

Supports running offline mock checks or live API verification for:
1) Google Gemma via AMD Token Factory;
2) Evolus Business Agents (Workflow + Knowledge Library);
3) End-to-end Dual-Prize unified Bellini smart-building incident flow.
"""
from __future__ import annotations

import argparse
import json
import sys

from .dual_prize import run_dual_prize_pipeline
from .evolus_adapter import evolus_smoke
from .token_factory_provider import token_factory_smoke


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="AMD ACT III Partner Track Verification Smoke Runner")
    parser.add_argument("--all", action="store_true", help="Run smoke tests for Gemma, Evolus, and Dual-Prize pipeline")
    parser.add_argument("--gemma", action="store_true", help="Run Gemma Token Factory smoke test")
    parser.add_argument("--evolus", action="store_true", help="Run Evolus Partner smoke test")
    parser.add_argument("--dual", action="store_true", help="Run full Dual-Prize unified incident pipeline")
    parser.add_argument("--live", action="store_true", help="Attempt live external API calls using configured keys")
    parser.add_argument("--json", action="store_true", help="Output machine-readable JSON only")

    args = parser.parse_args(argv)

    # Default to running --all in mock mode if no specific flags given
    if not (args.gemma or args.evolus or args.dual or args.all):
        args.all = True

    mock_mode = not args.live
    results: dict[str, object] = {
        "mode": "live" if args.live else "mock",
        "tracks": {},
    }

    if args.gemma or args.all:
        gemma_res = token_factory_smoke(mock=mock_mode)
        results["tracks"]["google_gemma"] = gemma_res

    if args.evolus or args.all:
        evolus_res = evolus_smoke(mock=mock_mode)
        results["tracks"]["evolus_partner"] = evolus_res

    if args.dual or args.all:
        dual_res = run_dual_prize_pipeline(gemma_mock=mock_mode, evolus_mock=mock_mode)
        results["tracks"]["dual_prize_pipeline"] = dual_res.manifest()

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print("======================================================================")
        print(" AMD HACKATHON ACT III — PARTNER TRACK VERIFICATION REPORT")
        print(f" Execution Mode: {'LIVE (external APIs)' if args.live else 'MOCK (deterministic offline)'}")
        print("======================================================================")
        for name, data in results["tracks"].items():
            print(f"\n--- Track: {name.upper()} ---")
            print(json.dumps(data, indent=2))
        print("\n======================================================================")

    return 0


if __name__ == "__main__":
    sys.exit(main())
