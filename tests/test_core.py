import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))

from inneros_act3.core import RouteRequest, route, verify_evidence


class RouterTests(unittest.TestCase):
    def test_privacy_forces_local(self):
        result = route(RouteRequest(privacy_required=True))
        self.assertEqual(result.target, 'amd-local')
        self.assertIn('privacy', result.reason_codes)

    def test_elastic_capacity_prefers_cloud(self):
        result = route(RouteRequest(needs_elastic_capacity=True))
        self.assertEqual(result.target, 'amd-cloud')
        self.assertIn('capability', result.reason_codes)

    def test_local_first_default(self):
        result = route(RouteRequest())
        self.assertEqual(result.target, 'amd-local')
        self.assertIn('local_first', result.reason_codes)

    def test_cloud_fallback(self):
        result = route(RouteRequest(local_available=False, cloud_available=True))
        self.assertEqual(result.target, 'amd-cloud')
        self.assertIn('fallback', result.reason_codes)

    def test_privacy_fails_closed(self):
        with self.assertRaises(RuntimeError):
            route(RouteRequest(privacy_required=True, local_available=False))

    def test_evidence_hash_verifies(self):
        result = route(RouteRequest(latency_sensitive=True))
        digest = result.sha256()
        self.assertTrue(verify_evidence(result, digest))
        self.assertFalse(verify_evidence(result, '0' * 64))


if __name__ == '__main__':
    unittest.main()
