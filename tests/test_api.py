"""
AgentCourt API Tests
Tests health, policy listing, and dispute filing against the live API.
"""
import json
import urllib.request
import urllib.error
import unittest

BASE_URL = "https://agentcourt-api-production.up.railway.app"


class TestHealth(unittest.TestCase):
    def test_health_returns_ok(self):
        resp = urllib.request.urlopen(f"{BASE_URL}/health", timeout=10)
        data = json.loads(resp.read())
        self.assertEqual(data["status"], "ok")

    def test_health_has_policies(self):
        resp = urllib.request.urlopen(f"{BASE_URL}/health", timeout=10)
        data = json.loads(resp.read())
        self.assertGreaterEqual(len(data.get("policies", [])), 7)


class TestPolicies(unittest.TestCase):
    def test_list_policies(self):
        resp = urllib.request.urlopen(f"{BASE_URL}/v1/policies", timeout=10)
        data = json.loads(resp.read())
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 7)

    def test_expected_policies_exist(self):
        resp = urllib.request.urlopen(f"{BASE_URL}/v1/policies", timeout=10)
        data = json.loads(resp.read())
        names = [p["name"] for p in data]
        expected = [
            "api-quality", "freelance-delivery", "milestone-payment",
            "bug-bounty", "sla-monitoring", "scope-dispute", "physical-commerce"
        ]
        for policy in expected:
            self.assertIn(policy, names)

    def test_get_policy_details(self):
        resp = urllib.request.urlopen(
            f"{BASE_URL}/v1/policies/api-quality", timeout=10)
        data = json.loads(resp.read())
        self.assertEqual(data["name"], "api-quality")
        self.assertIn("rules", data)


class TestDisputeFiling(unittest.TestCase):
    def _file_dispute(self, payload):
        body = json.dumps(payload).encode()
        req = urllib.request.Request(
            f"{BASE_URL}/v1/disputes",
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        try:
            resp = urllib.request.urlopen(req, timeout=10)
            return json.loads(resp.read()), resp.status
        except urllib.error.HTTPError as e:
            return json.loads(e.read() or b"{}"), e.code

    def test_api_quality_schema_mismatch(self):
        data, code = self._file_dispute({
            "claimant": "test-agent",
            "respondent": "test-api",
            "contract": {"parties": ["test-agent", "test-api"], "obligations": ["Return JSON"]},
            "claim": "Schema mismatch",
            "desired_remedy": "full_refund",
            "evidence": [{"type": "log", "source": "test", "timestamp": "2026-01-01T00:00:00Z", "claimed_fact": "XML returned"}],
            "policy": "api-quality",
            "metadata": {"response_received": True, "schema_matches": False}
        })
        # May get 402 if free tier exhausted, otherwise should get ruling
        if code == 200:
            self.assertEqual(data["ruling"], "full_refund")
        else:
            self.assertEqual(code, 402)


class TestOpenAPI(unittest.TestCase):
    def test_docs_available(self):
        resp = urllib.request.urlopen(f"{BASE_URL}/docs", timeout=10)
        self.assertEqual(resp.status, 200)

    def test_openapi_spec(self):
        resp = urllib.request.urlopen(f"{BASE_URL}/openapi.json", timeout=10)
        data = json.loads(resp.read())
        self.assertIn("paths", data)
        self.assertIn("/v1/disputes", data["paths"])
        self.assertIn("/v1/policies", data["paths"])
        self.assertIn("/health", data["paths"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
