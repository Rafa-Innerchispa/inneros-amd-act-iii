import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from inneros_act3.scenario import run_scenario, smart_building_incident_steps


class SmartBuildingScenarioTests(unittest.TestCase):
    def test_scenario_is_local_first_and_guarded(self):
        result = run_scenario()
        self.assertEqual(result.schema, "inneros.act3.scenario.v1")
        self.assertEqual(result.state, "CONTRACT-ONLY")
        self.assertTrue(result.all_mutations_guarded)
        self.assertGreater(result.total_human_time_returned_seconds, 0)

        mutation_receipts = [r for r in result.receipts if r.mutating]
        self.assertEqual(len(mutation_receipts), 1)
        self.assertTrue(mutation_receipts[0].requires_human_approval)

        local = [r for r in result.receipts if r.route_target == "amd-local"]
        self.assertGreaterEqual(len(local), 5)

    def test_each_step_has_unique_verifiable_execution_hash(self):
        result = run_scenario()
        hashes = [r.execution_sha256 for r in result.receipts]
        self.assertEqual(len(hashes), len(set(hashes)))
        self.assertTrue(all(len(value) == 64 for value in hashes))
        self.assertEqual(len(result.evidence_manifest["bundle_sha256"]), 64)

    def test_default_scenario_exercises_agents_and_skills(self):
        steps = smart_building_incident_steps()
        self.assertEqual(len(steps), 6)
        self.assertGreaterEqual(len({step.agent for step in steps}), 5)
        self.assertGreaterEqual(len({step.skill for step in steps}), 5)


if __name__ == "__main__":
    unittest.main()
