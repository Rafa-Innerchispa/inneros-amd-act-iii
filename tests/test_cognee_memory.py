import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from inneros_act3.cognee_memory import (
    CogneeMemoryConfig,
    CogneeSharedMemory,
    SharedMemoryFact,
    prove_cross_agent_memory,
)


class FakeCogneeTransport:
    def __init__(self):
        self.rows = []
        self.remember_calls = []
        self.recall_calls = []

    def remember(self, *, dataset, text, node_set):
        self.remember_calls.append((dataset, text, node_set))
        self.rows.append({"text": text})
        return {"ok": True}

    def recall(self, *, dataset, query, top_k):
        self.recall_calls.append((dataset, query, top_k))
        return self.rows[:top_k]


class CogneeSharedMemoryTests(unittest.TestCase):
    def setUp(self):
        self.transport = FakeCogneeTransport()
        self.memory = CogneeSharedMemory(
            config=CogneeMemoryConfig(
                base_url="https://example.invalid",
                api_key="test-only",
                dataset="inneros-personal-brain",
            ),
            transport=self.transport,
        )

    def _fact(self, **overrides):
        data = {
            "fact_id": "bellini-sfp1-los-verified",
            "site": "Bellini I-II",
            "statement": "SFP1 showed a verified LOS condition during the captured incident.",
            "source": "AG-60 verified finding",
            "verified": True,
            "safe_to_share": True,
            "metadata": {"incident": "act3-demo"},
        }
        data.update(overrides)
        return SharedMemoryFact(**data)

    def test_agent_a_can_write_and_agent_b_can_recall_same_dataset(self):
        proof = prove_cross_agent_memory(
            self.memory,
            fact=self._fact(),
            writer_agent="AG-60-network-engineer",
            reader_agent="gemma-incident-director",
            recall_query="What verified Bellini backbone finding do we remember?",
        )

        self.assertEqual(proof["state"], "PROVEN")
        self.assertEqual(proof["dataset"], "inneros-personal-brain")
        self.assertEqual(proof["writer_agent"], "AG-60-network-engineer")
        self.assertEqual(proof["reader_agent"], "gemma-incident-director")
        self.assertGreater(proof["recall_count"], 0)
        self.assertEqual(len(proof["fact_sha256"]), 64)
        self.assertEqual(len(self.transport.remember_calls), 1)
        self.assertEqual(len(self.transport.recall_calls), 1)

    def test_unverified_or_private_fact_is_rejected_before_transport(self):
        with self.assertRaisesRegex(ValueError, "verified_fact_required"):
            self.memory.remember_verified_fact(
                self._fact(verified=False),
                writer_agent="AG-60",
            )
        with self.assertRaisesRegex(ValueError, "safe_to_share_required"):
            self.memory.remember_verified_fact(
                self._fact(safe_to_share=False),
                writer_agent="AG-60",
            )
        self.assertEqual(self.transport.remember_calls, [])

    def test_sensitive_metadata_key_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "sensitive_metadata_not_allowed"):
            self.memory.remember_verified_fact(
                self._fact(metadata={"api_key": "must-not-cross"}),
                writer_agent="AG-60",
            )

    def test_missing_runtime_credentials_fail_closed_without_fake_live_state(self):
        memory = CogneeSharedMemory(
            config=CogneeMemoryConfig(
                base_url="https://api.cognee.ai",
                api_key="",
                dataset="inneros-personal-brain",
            )
        )
        self.assertFalse(memory.ready)
        with self.assertRaisesRegex(RuntimeError, "cognee_not_configured"):
            memory.recall("Bellini", reader_agent="demo-agent")


if __name__ == "__main__":
    unittest.main()
