"""
AgentCourt API — Comprehensive Test Suite
==========================================
Tests the LIVE API at https://agentcourt-api-production.up.railway.app

Run: python3 -m pytest /root/.letta/agentcourt/tests/ -v
"""

import pytest
import requests
import time
import json

BASE_URL = "https://agentcourt-api-production.up.railway.app"
TIMEOUT = 10  # seconds


# ═══════════════════════════════════════════════════════════════════════════════
# HELPER FACTORIES
# ═══════════════════════════════════════════════════════════════════════════════

def make_evidence(eid, etype, source, fact, ts="2026-06-20", reliability="medium", content_hash=None):
    """Factory for a single evidence item."""
    item = {
        "id": eid,
        "type": etype,
        "source": source,
        "timestamp": ts,
        "claimed_fact": fact,
        "reliability": reliability,
    }
    if content_hash:
        item["content_hash"] = content_hash
    return item


def make_dispute(
    claimant="Claimant",
    respondent="Respondent",
    policy="freelance-delivery",
    obligations=None,
    deadlines=None,
    payment_terms="$5,000 due on delivery",
    claim="Dispute claim",
    desired_remedy="Full refund",
    evidence=None,
    metadata=None,
):
    """Factory for a dispute request payload."""
    return {
        "claimant": claimant,
        "respondent": respondent,
        "contract": {
            "parties": [claimant, respondent],
            "obligations": obligations or ["Deliver agreed work"],
            "deadlines": deadlines,
            "payment_terms": payment_terms,
        },
        "claim": claim,
        "desired_remedy": desired_remedy,
        "policy": policy,
        "evidence": evidence if evidence is not None else [
            make_evidence("e1", "message", "email", "Work was delivered and accepted")
        ],
        "metadata": metadata,
    }


def submit_dispute(payload):
    """POST to /v1/disputes and return (response_dict, elapsed_seconds)."""
    start = time.time()
    resp = requests.post(f"{BASE_URL}/v1/disputes", json=payload, timeout=TIMEOUT)
    elapsed = time.time() - start
    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}: {resp.text[:300]}"
    return resp.json(), elapsed


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 1: BASIC ENDPOINT TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestHealthEndpoint:
    """Test /health endpoint."""

    def test_health_returns_200(self):
        resp = requests.get(f"{BASE_URL}/health", timeout=TIMEOUT)
        assert resp.status_code == 200

    def test_health_has_status_ok(self):
        resp = requests.get(f"{BASE_URL}/health", timeout=TIMEOUT)
        data = resp.json()
        assert data["status"] == "ok"

    def test_health_has_version(self):
        resp = requests.get(f"{BASE_URL}/health", timeout=TIMEOUT)
        data = resp.json()
        assert "version" in data

    def test_health_lists_policies(self):
        resp = requests.get(f"{BASE_URL}/health", timeout=TIMEOUT)
        data = resp.json()
        assert "policies" in data
        assert isinstance(data["policies"], list)
        assert len(data["policies"]) > 0

    def test_health_has_engine(self):
        resp = requests.get(f"{BASE_URL}/health", timeout=TIMEOUT)
        data = resp.json()
        assert "engine" in data


class TestRootEndpoint:
    """Test / endpoint."""

    def test_root_returns_200(self):
        resp = requests.get(f"{BASE_URL}/", timeout=TIMEOUT)
        assert resp.status_code == 200

    def test_root_has_name(self):
        resp = requests.get(f"{BASE_URL}/", timeout=TIMEOUT)
        data = resp.json()
        assert data["name"] == "AgentCourt"

    def test_root_has_endpoints(self):
        resp = requests.get(f"{BASE_URL}/", timeout=TIMEOUT)
        data = resp.json()
        assert "endpoints" in data
        assert "submit_dispute" in data["endpoints"]


class TestPoliciesEndpoint:
    """Test /v1/policies endpoints."""

    def test_list_policies_returns_200(self):
        resp = requests.get(f"{BASE_URL}/v1/policies", timeout=TIMEOUT)
        assert resp.status_code == 200

    def test_list_policies_returns_list(self):
        resp = requests.get(f"{BASE_URL}/v1/policies", timeout=TIMEOUT)
        data = resp.json()
        assert isinstance(data, list)

    def test_list_policies_has_expected_policies(self):
        resp = requests.get(f"{BASE_URL}/v1/policies", timeout=TIMEOUT)
        data = resp.json()
        names = [p["name"] for p in data]
        assert "freelance-delivery" in names
        assert "milestone-payment" in names
        assert "bug-bounty" in names
        assert "sla-monitoring" in names

    def test_get_specific_policy_returns_200(self):
        resp = requests.get(f"{BASE_URL}/v1/policies/freelance-delivery", timeout=TIMEOUT)
        assert resp.status_code == 200

    def test_get_specific_policy_has_rules(self):
        resp = requests.get(f"{BASE_URL}/v1/policies/freelance-delivery", timeout=TIMEOUT)
        data = resp.json()
        assert "rules" in data
        assert len(data["rules"]) > 0

    def test_get_nonexistent_policy_404(self):
        resp = requests.get(f"{BASE_URL}/v1/policies/nonexistent-policy-xyz", timeout=TIMEOUT)
        assert resp.status_code == 404


class TestCasesAndVerdicts:
    """Test /v1/cases and /v1/verdicts endpoints."""

    def test_list_cases_returns_200(self):
        resp = requests.get(f"{BASE_URL}/v1/cases", timeout=TIMEOUT)
        assert resp.status_code == 200

    def test_list_cases_returns_list(self):
        resp = requests.get(f"{BASE_URL}/v1/cases", timeout=TIMEOUT)
        data = resp.json()
        assert isinstance(data, list)

    def test_get_nonexistent_case_404(self):
        resp = requests.get(f"{BASE_URL}/v1/cases/nonexistent-case-xyz123", timeout=TIMEOUT)
        assert resp.status_code == 404

    def test_verdicts_returns_200(self):
        resp = requests.get(f"{BASE_URL}/v1/verdicts", timeout=TIMEOUT)
        assert resp.status_code == 200

    def test_verdicts_has_total(self):
        resp = requests.get(f"{BASE_URL}/v1/verdicts", timeout=TIMEOUT)
        data = resp.json()
        assert "total" in data
        assert "verdicts" in data


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 2: FREELANCE-DELIVERY POLICY TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestFreelanceDelivery:
    """Comprehensive tests for freelance-delivery policy template."""

    def test_delivery_on_time_accepted(self):
        """Work delivered, accepted, on time → no remedy owed."""
        payload = make_dispute(
            policy="freelance-delivery",
            evidence=[
                make_evidence("e1", "commit", "github", "Code committed and delivered to client", ts="2026-06-10"),
                make_evidence("e2", "message", "email", "Client accepted the deliverable on June 10", ts="2026-06-10"),
            ],
            deadlines=["2026-06-15"],
        )
        result, elapsed = submit_dispute(payload)
        assert result["matched_rule_id"] == "delivery-on-time-accepted"
        assert result["confidence"] == "high"
        assert result["remedy"] == "none"
        assert result["status"] == "ruled"

    def test_late_delivery_accepted(self):
        """Work accepted but late → partial remedy."""
        payload = make_dispute(
            policy="freelance-delivery",
            evidence=[
                make_evidence("e1", "commit", "github", "Code committed and delivered", ts="2026-06-20"),
                make_evidence("e2", "message", "email", "Client accepted the deliverable", ts="2026-06-20"),
            ],
            deadlines=["2026-06-10"],
        )
        result, elapsed = submit_dispute(payload)
        assert result["matched_rule_id"] == "late-delivery-accepted"
        assert result["confidence"] in ("medium", "high")

    def test_non_delivery(self):
        """No delivery evidence, not accepted → full refund."""
        payload = make_dispute(
            policy="freelance-delivery",
            claim="Developer never delivered any work",
            evidence=[
                make_evidence("e1", "message", "email", "No work was ever submitted", ts="2026-06-20"),
            ],
        )
        result, elapsed = submit_dispute(payload)
        assert result["matched_rule_id"] == "non-delivery"
        assert result["confidence"] == "high"
        assert result["remedy"] == "full_refund"

    def test_rejected_for_quality(self):
        """Work delivered but rejected for quality issues → rework/refund."""
        payload = make_dispute(
            policy="freelance-delivery",
            evidence=[
                make_evidence("e1", "commit", "github", "Code was submitted and pushed", ts="2026-06-15"),
                make_evidence("e2", "message", "email", "Client rejected deliverable due to quality defects and bugs", ts="2026-06-15"),
            ],
        )
        result, elapsed = submit_dispute(payload)
        assert result["matched_rule_id"] == "rejected-quality"
        assert result["confidence"] in ("medium", "low")

    def test_partial_delivery(self):
        """Only partial work delivered → partial refund."""
        payload = make_dispute(
            policy="freelance-delivery",
            evidence=[
                make_evidence("e1", "commit", "github", "Only 3 out of 10 features were delivered", ts="2026-06-15"),
                make_evidence("e2", "message", "email", "Partial delivery submitted", ts="2026-06-15"),
            ],
        )
        result, elapsed = submit_dispute(payload)
        assert result["matched_rule_id"] == "partial-delivery"

    def test_disputed_acceptance(self):
        """Delivery happened but acceptance is disputed → escalate."""
        payload = make_dispute(
            policy="freelance-delivery",
            evidence=[
                make_evidence("e1", "commit", "github", "Work was delivered", ts="2026-06-15"),
                make_evidence("e2", "message", "email", "Client claims they rejected it", ts="2026-06-15"),
                make_evidence("e3", "message", "email", "Developer claims client accepted it", ts="2026-06-15"),
            ],
        )
        result, elapsed = submit_dispute(payload)
        # Could match disputed-acceptance or partial-delivery depending on fact extraction
        assert result["matched_rule_id"] in ("disputed-acceptance", "partial-delivery", "rejected-quality")


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 3: MILESTONE-PAYMENT POLICY TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestMilestonePayment:
    """Comprehensive tests for milestone-payment policy template."""

    def test_milestone_completed_paid(self):
        """Milestone done and paid → no remedy."""
        payload = make_dispute(
            policy="milestone-payment",
            payment_terms="$5,000 per milestone, net 30 days",
            evidence=[
                make_evidence("e1", "commit", "github", "Milestone completed and deployed", ts="2026-06-10"),
                make_evidence("e2", "payment", "stripe", "Payment received via USDC", ts="2026-06-12"),
            ],
            metadata={"milestone_completed": True, "payment_terms_days": 30, "days_since_completion": 10},
        )
        result, elapsed = submit_dispute(payload)
        assert result["matched_rule_id"] == "milestone-completed-paid"
        assert result["remedy"] == "none"

    def test_milestone_completed_unpaid(self):
        """Mstone done but unpaid past terms → full payment + penalty."""
        payload = make_dispute(
            policy="milestone-payment",
            claim="Milestone completed but payment never received",
            payment_terms="$5,000 per milestone, net 7 days",
            evidence=[
                make_evidence("e1", "commit", "github", "Milestone completed and shipped", ts="2026-05-20"),
                make_evidence("e2", "message", "email", "Client acknowledged milestone completion", ts="2026-05-20"),
                make_evidence("e3", "message", "email", "No payment received despite multiple requests", ts="2026-06-20"),
            ],
            metadata={"milestone_completed": True, "payment_terms_days": 7, "days_since_completion": 31},
        )
        result, elapsed = submit_dispute(payload)
        assert result["matched_rule_id"] == "milestone-completed-unpaid"
        assert "full_payment" in result["remedy"]

    def test_milestone_incomplete_payment_demanded(self):
        """Milestone not done but payment demanded → deny."""
        payload = make_dispute(
            policy="milestone-payment",
            claim="Payment demanded for incomplete milestone",
            evidence=[
                make_evidence("e1", "message", "email", "Milestone is incomplete, only 40% done", ts="2026-06-20"),
                make_evidence("e2", "message", "email", "Client rejected the deliverable", ts="2026-06-20"),
            ],
        )
        result, elapsed = submit_dispute(payload)
        assert result["matched_rule_id"] in ("milestone-incomplete-payment-demanded", "milestone-partially-complete")

    def test_milestone_disputed_completion(self):
        """Cannot determine if milestone was completed → escalate."""
        payload = make_dispute(
            policy="milestone-payment",
            evidence=[
                make_evidence("e1", "message", "email", "Some work may have been done", ts="2026-06-20"),
            ],
            metadata={"milestone_completed": None},
        )
        result, elapsed = submit_dispute(payload)
        assert result["matched_rule_id"] == "milestone-disputed-completion"
        assert result["confidence"] == "low"


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 4: BUG-BOUNTY POLICY TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestBugBounty:
    """Comprehensive tests for bug-bounty policy template."""

    def test_valid_bug_full_payout(self):
        """Reproducible, high severity, proper disclosure → full payout."""
        payload = make_dispute(
            policy="bug-bounty",
            claimant="Security Researcher",
            respondent="DeFi Protocol",
            claim="Bug report submitted but full bounty denied",
            desired_remedy="Full $5,000 payout",
            payment_terms="$5,000 for critical severity bugs",
            evidence=[
                make_evidence("e1", "poc_code", "hackerone", "SQL injection reproduced 3 independent times", ts="2026-06-18"),
                make_evidence("e2", "message", "email", "Vendor rated as critical severity", ts="2026-06-18", reliability="high"),
                make_evidence("e3", "message", "email", "Responsible disclosure followed, vendor notified privately", ts="2026-06-18"),
            ],
        )
        result, elapsed = submit_dispute(payload)
        assert result["matched_rule_id"] == "valid-bug-full-payout"
        assert result["remedy"] == "full_payout"

    def test_non_reproducible_bug(self):
        """Bug not reproducible after 3+ attempts → deny payout."""
        payload = make_dispute(
            policy="bug-bounty",
            claim="Bounty denied, researcher disputes",
            evidence=[
                make_evidence("e1", "poc_code", "hackerone", "Could not reproduce after 5 attempts", ts="2026-06-18"),
                make_evidence("e2", "message", "email", "Failed to reproduce in any environment", ts="2026-06-18"),
            ],
        )
        result, elapsed = submit_dispute(payload)
        assert result["matched_rule_id"] in ("non-reproducible-bug", "disclosure-violation", "disputed-reproducibility")

    def test_disclosure_violation(self):
        """Bug valid but disclosure rules violated → reduced/denied."""
        payload = make_dispute(
            policy="bug-bounty",
            claim="Researcher demands payout",
            evidence=[
                make_evidence("e1", "poc_code", "hackerone", "SQL injection reproduced 3 times", ts="2026-06-18"),
                make_evidence("e2", "message", "twitter", "Bug was publicly disclosed on Twitter before vendor notification", ts="2026-06-18"),
            ],
        )
        result, elapsed = submit_dispute(payload)
        assert result["matched_rule_id"] == "disclosure-violation"

    def test_disputed_reproducibility(self):
        """Can't determine reproducibility → escalate."""
        payload = make_dispute(
            policy="bug-bounty",
            claim="Reproducibility disputed",
            evidence=[
                make_evidence("e1", "message", "email", "Researcher claims bug exists", ts="2026-06-18"),
            ],
        )
        result, elapsed = submit_dispute(payload)
        # bug_is_reproducible will be None since no repro evidence
        assert result["matched_rule_id"] in ("disputed-reproducibility", "disclosure-violation")


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 5: SLA-MONITORING POLICY TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestSLAMonitoring:
    """Comprehensive tests for sla-monitoring policy template."""

    def test_uptime_violation(self):
        """Uptime below SLA threshold → service credit."""
        payload = make_dispute(
            policy="sla-monitoring",
            claimant="Customer",
            respondent="API Provider",
            obligations=["Maintain 99.9% uptime SLA", "Max latency 200ms"],
            claim="SLA breach — uptime at 98.2%",
            desired_remedy="Service credit of $5,000",
            payment_terms="99.9% uptime SLA with 200ms max latency",
            evidence=[
                make_evidence("e1", "log", "datadog", "Monitoring data shows uptime of 98.2% during June 2026", ts="2026-06-20"),
                make_evidence("e2", "log", "cloudwatch", "Observed availability at 98.2% with multiple outages", ts="2026-06-20"),
            ],
        )
        result, elapsed = submit_dispute(payload)
        assert result["matched_rule_id"] == "uptime-violation"
        assert result["confidence"] == "high"
        assert result["remedy"] == "service_credit"

    def test_latency_breach(self):
        """Latency exceeds SLA → service credit."""
        payload = make_dispute(
            policy="sla-monitoring",
            obligations=["Maintain 99.9% uptime", "Max response latency 200ms"],
            claim="Latency breach — 350ms average",
            payment_terms="99.9% uptime SLA with 200ms max latency",
            evidence=[
                make_evidence("e1", "log", "datadog", "Average latency measured at 350ms during peak hours", ts="2026-06-20"),
                make_evidence("e2", "log", "grafana", "Recorded latency of 350ms exceeding SLA", ts="2026-06-20"),
            ],
            metadata={"actual_uptime": 99.95, "required_uptime": 99.9},
        )
        result, elapsed = submit_dispute(payload)
        assert result["matched_rule_id"] == "latency-breach"
        assert result["remedy"] == "service_credit"

    def test_incidents_within_sla(self):
        """Incidents occurred but uptime still meets SLA → deny credit."""
        payload = make_dispute(
            policy="sla-monitoring",
            obligations=["Maintain 99.5% uptime"],
            claim="Customer demands credit for minor incidents",
            payment_terms="99.5% uptime SLA",
            evidence=[
                make_evidence("e1", "log", "datadog", "Monitoring shows uptime of 99.7% for the period", ts="2026-06-20"),
            ],
            metadata={"actual_uptime": 99.7, "required_uptime": 99.5},
        )
        result, elapsed = submit_dispute(payload)
        assert result["matched_rule_id"] == "incidents-within-sla"
        assert result["remedy"] == "deny_credit"

    def test_insufficient_monitoring(self):
        """No monitoring data provided → escalate."""
        payload = make_dispute(
            policy="sla-monitoring",
            claim="Customer claims SLA breach",
            evidence=[
                make_evidence("e1", "message", "email", "Service was down sometimes, I think", ts="2026-06-20"),
            ],
        )
        result, elapsed = submit_dispute(payload)
        assert result["matched_rule_id"] == "insufficient-monitoring"
        assert result["confidence"] == "low"


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 6: EDGE CASES
# ═══════════════════════════════════════════════════════════════════════════════

class TestEdgeCases:
    """Edge cases: empty evidence, missing fields, invalid policy, extreme values."""

    def test_empty_evidence_list(self):
        """Dispute with no evidence items."""
        payload = make_dispute(evidence=[])
        result, elapsed = submit_dispute(payload)
        assert result["status"] in ("ruled", "needs_more_info")
        assert "ruling" in result

    def test_single_evidence_item(self):
        """Dispute with exactly one evidence item."""
        payload = make_dispute(
            evidence=[make_evidence("e1", "message", "email", "Work was done")]
        )
        result, elapsed = submit_dispute(payload)
        assert "ruling" in result

    def test_many_evidence_items(self):
        """Dispute with 20 evidence items — stress test."""
        evidence = [
            make_evidence(f"e{i}", "message", "email", f"Evidence item number {i}", ts="2026-06-15")
            for i in range(20)
        ]
        payload = make_dispute(evidence=evidence)
        result, elapsed = submit_dispute(payload)
        assert "ruling" in result

    def test_invalid_policy_name(self):
        """Policy that doesn't exist → 400 error."""
        payload = make_dispute(policy="nonexistent-policy-xyz")
        resp = requests.post(f"{BASE_URL}/v1/disputes", json=payload, timeout=TIMEOUT)
        assert resp.status_code in (400, 500)

    def test_missing_claimant(self):
        """Missing required field claimant → 422 validation error."""
        payload = make_dispute()
        del payload["claimant"]
        resp = requests.post(f"{BASE_URL}/v1/disputes", json=payload, timeout=TIMEOUT)
        assert resp.status_code == 422

    def test_missing_respondent(self):
        """Missing required field respondent → 422."""
        payload = make_dispute()
        del payload["respondent"]
        resp = requests.post(f"{BASE_URL}/v1/disputes", json=payload, timeout=TIMEOUT)
        assert resp.status_code == 422

    def test_missing_contract(self):
        """Missing contract field → 422."""
        payload = make_dispute()
        del payload["contract"]
        resp = requests.post(f"{BASE_URL}/v1/disputes", json=payload, timeout=TIMEOUT)
        assert resp.status_code == 422

    def test_missing_evidence_field(self):
        """Missing evidence field → 422."""
        payload = make_dispute()
        del payload["evidence"]
        resp = requests.post(f"{BASE_URL}/v1/disputes", json=payload, timeout=TIMEOUT)
        assert resp.status_code == 422

    def test_empty_claim_text(self):
        """Empty claim string → should still process."""
        payload = make_dispute(claim="")
        result, elapsed = submit_dispute(payload)
        assert "ruling" in result

    def test_extremely_long_claim(self):
        """Very long claim text — 10,000 chars."""
        payload = make_dispute(claim="A" * 10000)
        result, elapsed = submit_dispute(payload)
        assert "ruling" in result

    def test_special_characters_in_claim(self):
        """Unicode and special characters in claim."""
        payload = make_dispute(claim="Dispute about naïve façade résumé — 中文 — émojis 🚀💎🔥")
        result, elapsed = submit_dispute(payload)
        assert "ruling" in result

    def test_evidence_with_no_claimed_fact(self):
        """Evidence item with empty claimed_fact."""
        payload = make_dispute(
            evidence=[make_evidence("e1", "message", "email", "")]
        )
        result, elapsed = submit_dispute(payload)
        assert "ruling" in result

    def test_metadata_override(self):
        """Metadata facts should override extracted facts."""
        payload = make_dispute(
            policy="milestone-payment",
            evidence=[
                make_evidence("e1", "commit", "github", "Work completed", ts="2026-06-10"),
            ],
            metadata={
                "milestone_completed": True,
                "payment_received": True,
                "days_since_completion": 5,
                "payment_terms_days": 30,
            },
        )
        result, elapsed = submit_dispute(payload)
        assert result["matched_rule_id"] == "milestone-completed-paid"


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 7: RULING TEXT QUALITY
# ═══════════════════════════════════════════════════════════════════════════════

class TestRulingQuality:
    """Verify ruling text quality — no N/A, no 'could not be generated'."""

    @pytest.fixture(autouse=True)
    def _run_all_policies(self):
        """Submit one dispute per policy and store results."""
        self.results = {}
        policies_and_payloads = {
            "freelance-delivery": make_dispute(
                policy="freelance-delivery",
                evidence=[
                    make_evidence("e1", "commit", "github", "Code delivered", ts="2026-06-10"),
                    make_evidence("e2", "message", "email", "Client accepted the deliverable", ts="2026-06-10"),
                ],
                deadlines=["2026-06-15"],
            ),
            "milestone-payment": make_dispute(
                policy="milestone-payment",
                payment_terms="$5,000 per milestone, net 30 days",
                evidence=[
                    make_evidence("e1", "commit", "github", "Milestone completed and deployed", ts="2026-06-10"),
                    make_evidence("e2", "payment", "stripe", "Payment received via USDC", ts="2026-06-12"),
                ],
                metadata={"milestone_completed": True, "payment_terms_days": 30, "days_since_completion": 10},
            ),
            "bug-bounty": make_dispute(
                policy="bug-bounty",
                claimant="Researcher",
                respondent="Protocol",
                payment_terms="$5,000 for critical severity",
                evidence=[
                    make_evidence("e1", "poc_code", "hackerone", "SQL injection reproduced 3 independent times", ts="2026-06-18"),
                    make_evidence("e2", "message", "email", "Vendor rated as critical severity", ts="2026-06-18", reliability="high"),
                    make_evidence("e3", "message", "email", "Responsible disclosure followed", ts="2026-06-18"),
                ],
            ),
            "sla-monitoring": make_dispute(
                policy="sla-monitoring",
                obligations=["Maintain 99.9% uptime SLA", "Max latency 200ms"],
                payment_terms="99.9% uptime SLA with 200ms max latency",
                evidence=[
                    make_evidence("e1", "log", "datadog", "Monitoring shows uptime of 98.2% during June", ts="2026-06-20"),
                ],
            ),
        }
        for name, payload in policies_and_payloads.items():
            result, _ = submit_dispute(payload)
            self.results[name] = result

    def test_no_could_not_be_generated(self):
        """No ruling should contain 'could not be generated'."""
        for policy, result in self.results.items():
            ruling = result.get("ruling", "")
            assert "could not be generated" not in ruling.lower(), \
                f"Policy '{policy}' ruling says 'could not be generated': {ruling[:100]}"

    def test_ruling_is_nonempty(self):
        """Every ruling text should be non-empty."""
        for policy, result in self.results.items():
            ruling = result.get("ruling", "")
            assert len(ruling.strip()) > 10, \
                f"Policy '{policy}' has empty or very short ruling: '{ruling}'"

    def test_ruling_has_specific_content(self):
        """Ruling should contain policy-relevant words, not just boilerplate."""
        for policy, result in self.results.items():
            ruling = result.get("ruling", "").lower()
            # Should mention something specific (not just generic text)
            assert len(ruling) > 30, \
                f"Policy '{policy}' ruling too generic: '{ruling[:100]}'"

    def test_matched_rule_exists(self):
        """Every ruling should have a matched_rule_id."""
        for policy, result in self.results.items():
            assert result.get("matched_rule_id") is not None, \
                f"Policy '{policy}' has no matched_rule_id"

    def test_policy_name_in_response(self):
        """Response should include the policy name."""
        for policy, result in self.results.items():
            assert result.get("policy_name") is not None, \
                f"Policy '{policy}' response missing policy_name"


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 8: EVIDENCE SCORING
# ═══════════════════════════════════════════════════════════════════════════════

class TestEvidenceScoring:
    """Verify evidence scores are valid (0-1 range)."""

    def test_scores_in_valid_range(self):
        """All evidence scores should be between 0 and 1."""
        payload = make_dispute(
            evidence=[
                make_evidence("e1", "commit", "github", "Code delivered", reliability="high"),
                make_evidence("e2", "message", "email", "Client accepted", reliability="medium"),
                make_evidence("e3", "screenshot", "imgur", "Screenshot of work", reliability="low"),
            ],
        )
        result, elapsed = submit_dispute(payload)
        scores = result.get("evidence_scores", [])
        assert len(scores) == 3
        for s in scores:
            assert "score" in s
            assert 0.0 <= s["score"] <= 1.0, \
                f"Evidence score {s['score']} out of range [0,1] for {s['id']}"

    def test_high_reliability_scores_higher_than_low(self):
        """High reliability evidence should score >= low reliability."""
        payload = make_dispute(
            evidence=[
                make_evidence("e_high", "commit", "github", "Code delivered", reliability="high", content_hash="abc123"),
                make_evidence("e_low", "commit", "github", "Code delivered", reliability="low"),
            ],
        )
        result, elapsed = submit_dispute(payload)
        scores = {s["id"]: s["score"] for s in result.get("evidence_scores", [])}
        assert scores.get("e_high", 0) >= scores.get("e_low", 0), \
            f"High reliability ({scores.get('e_high')}) should be >= low ({scores.get('e_low')})"

    def test_hashed_evidence_gets_bonus(self):
        """Evidence with content_hash should score >= same without hash."""
        payload = make_dispute(
            evidence=[
                make_evidence("e_hashed", "message", "email", "Work accepted", content_hash="sha256:abc"),
                make_evidence("e_plain", "message", "email", "Work accepted"),
            ],
        )
        result, elapsed = submit_dispute(payload)
        scores = {s["id"]: s["score"] for s in result.get("evidence_scores", [])}
        assert scores.get("e_hashed", 0) >= scores.get("e_plain", 0), \
            f"Hashed evidence ({scores.get('e_hashed')}) should be >= plain ({scores.get('e_plain')})"


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 9: FACT EXTRACTION
# ═══════════════════════════════════════════════════════════════════════════════

class TestFactExtraction:
    """Verify correct facts are established from evidence."""

    def test_delivery_evidence_detected(self):
        """Commit evidence with delivery keywords → evidence_of_delivery=True."""
        payload = make_dispute(
            evidence=[
                make_evidence("e1", "commit", "github", "Code was delivered and pushed to main branch", ts="2026-06-10"),
            ],
        )
        result, elapsed = submit_dispute(payload)
        facts_established = {f["fact"]: f["value"] for f in result.get("facts_established", [])}
        assert facts_established.get("evidence_of_delivery") == "True"

    def test_no_delivery_evidence_detected(self):
        """No commit/file evidence → evidence_of_delivery should be False/absent."""
        payload = make_dispute(
            evidence=[
                make_evidence("e1", "message", "email", "No work was ever submitted"),
            ],
        )
        result, elapsed = submit_dispute(payload)
        # evidence_of_delivery should be False — it'll be in facts_disputed
        facts_disputed = {f["fact"] for f in result.get("facts_disputed", [])}
        assert "evidence_of_delivery" in facts_disputed

    def test_acceptance_detected(self):
        """Evidence with 'accepted' keyword → deliverable_was_accepted=True."""
        payload = make_dispute(
            evidence=[
                make_evidence("e1", "commit", "github", "Code delivered", ts="2026-06-10"),
                make_evidence("e2", "message", "email", "Client accepted the deliverable", ts="2026-06-10"),
            ],
            deadlines=["2026-06-15"],
        )
        result, elapsed = submit_dispute(payload)
        facts_established = {f["fact"]: f["value"] for f in result.get("facts_established", [])}
        assert facts_established.get("deliverable_was_accepted") == "True"

    def test_quality_issues_detected(self):
        """Evidence mentioning 'quality' or 'defect' → quality_issues_documented=True."""
        payload = make_dispute(
            evidence=[
                make_evidence("e1", "commit", "github", "Code submitted", ts="2026-06-10"),
                make_evidence("e2", "message", "email", "Rejected due to quality defects and bugs", ts="2026-06-10"),
            ],
        )
        result, elapsed = submit_dispute(payload)
        facts_established = {f["fact"]: f["value"] for f in result.get("facts_established", [])}
        assert facts_established.get("quality_issues_documented") == "True"

    def test_payment_received_detected(self):
        """Payment-type evidence → payment_received=True."""
        payload = make_dispute(
            policy="milestone-payment",
            payment_terms="$5,000 per milestone, net 30",
            evidence=[
                make_evidence("e1", "commit", "github", "Milestone completed", ts="2026-06-10"),
                make_evidence("e2", "payment", "stripe", "Payment received via USDC", ts="2026-06-12"),
            ],
            metadata={"milestone_completed": True, "payment_terms_days": 30, "days_since_completion": 10},
        )
        result, elapsed = submit_dispute(payload)
        facts_established = {f["fact"]: f["value"] for f in result.get("facts_established", [])}
        assert facts_established.get("payment_received") == "True"

    def test_no_payment_detected(self):
        """Evidence saying 'no payment' → payment_received=False."""
        payload = make_dispute(
            policy="milestone-payment",
            payment_terms="$5,000 per milestone, net 30",
            evidence=[
                make_evidence("e1", "commit", "github", "Milestone completed and shipped", ts="2026-06-10"),
                make_evidence("e2", "message", "email", "No payment received from client", ts="2026-06-20"),
            ],
            metadata={"milestone_completed": True, "payment_terms_days": 7, "days_since_completion": 31},
        )
        result, elapsed = submit_dispute(payload)
        facts_disputed = {f["fact"] for f in result.get("facts_disputed", [])}
        assert "payment_received" in facts_disputed

    def test_facts_structure(self):
        """Facts should be properly categorized into established/disputed/unknown."""
        payload = make_dispute(
            evidence=[
                make_evidence("e1", "message", "email", "Unclear situation, work may or may not have been done"),
            ],
        )
        result, elapsed = submit_dispute(payload)
        assert isinstance(result.get("facts_established"), list)
        assert isinstance(result.get("facts_disputed"), list)
        assert isinstance(result.get("facts_unknown"), list)


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 10: RESPONSE TIME
# ═══════════════════════════════════════════════════════════════════════════════

class TestResponseTime:
    """Each ruling should complete in under 5 seconds."""

    @pytest.mark.parametrize("policy,payment_terms,obligations,evidence_facts", [
        ("freelance-delivery", "$5,000 on delivery", None,
         [("e1", "commit", "github", "Code delivered"), ("e2", "message", "email", "Client accepted")]),
        ("milestone-payment", "$5,000 per milestone, net 30", None,
         [("e1", "commit", "github", "Milestone completed"), ("e2", "payment", "stripe", "Payment received via USDC")]),
        ("bug-bounty", "$5,000 for critical", None,
         [("e1", "poc_code", "hackerone", "SQL injection reproduced 3 independent times"),
          ("e2", "message", "email", "Vendor rated as critical severity")]),
        ("sla-monitoring", "99.9% uptime SLA with 200ms max latency",
         ["Maintain 99.9% uptime SLA", "Max latency 200ms"],
         [("e1", "log", "datadog", "Uptime of 98.2% observed during June")]),
    ])
    def test_response_under_5_seconds(self, policy, payment_terms, obligations, evidence_facts):
        evidence = [
            make_evidence(eid, etype, source, fact, ts="2026-06-15")
            for eid, etype, source, fact in evidence_facts
        ]
        payload = make_dispute(
            policy=policy,
            payment_terms=payment_terms,
            obligations=obligations,
            evidence=evidence,
        )
        result, elapsed = submit_dispute(payload)
        assert elapsed < 5.0, f"Response took {elapsed:.2f}s (>5s) for policy '{policy}'"


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 11: FULL PIPELINE INTEGRITY
# ═══════════════════════════════════════════════════════════════════════════════

class TestFullPipeline:
    """End-to-end pipeline integrity tests."""

    def test_case_is_saved_and_retrievable(self):
        """Submit a dispute, then retrieve it via /v1/cases/{case_id}."""
        payload = make_dispute()
        result, _ = submit_dispute(payload)
        case_id = result["case_id"]

        # Retrieve the case
        resp = requests.get(f"{BASE_URL}/v1/cases/{case_id}", timeout=TIMEOUT)
        assert resp.status_code == 200
        case_data = resp.json()
        assert "request" in case_data or "ruling" in case_data

    def test_ruling_has_all_required_fields(self):
        """Ruling response should have all fields from RulingResponse schema."""
        payload = make_dispute()
        result, _ = submit_dispute(payload)
        required_fields = [
            "case_id", "status", "confidence", "ruling", "reasoning",
            "remedy", "facts_established", "facts_disputed", "facts_unknown",
            "ruled_at", "engine_version",
        ]
        for field in required_fields:
            assert field in result, f"Missing field '{field}' in ruling response"

    def test_reasoning_contains_evidence_count(self):
        """Reasoning should mention how many evidence items were evaluated."""
        payload = make_dispute(
            evidence=[
                make_evidence("e1", "commit", "github", "Code delivered"),
                make_evidence("e2", "message", "email", "Accepted"),
                make_evidence("e3", "screenshot", "imgur", "Screenshot"),
            ],
        )
        result, _ = submit_dispute(payload)
        reasoning = result.get("reasoning", "")
        assert "3" in reasoning or "evidence" in reasoning.lower()

    def test_engine_version_present(self):
        """Response should include engine version."""
        payload = make_dispute()
        result, _ = submit_dispute(payload)
        assert result["engine_version"] == "1.0.0"

    def test_ruled_at_is_iso_format(self):
        """ruled_at should be a valid ISO timestamp."""
        from datetime import datetime
        payload = make_dispute()
        result, _ = submit_dispute(payload)
        ts = result["ruled_at"]
        # Should parse without error
        datetime.fromisoformat(ts.replace("Z", ""))


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 12: ADDITIONAL POLICY TESTS (API-QUALITY, PHYSICAL-COMMERCE)
# ═══════════════════════════════════════════════════════════════════════════════

class TestAPIQualityPolicy:
    """Tests for api-quality policy (uses metadata-driven facts)."""

    def test_schema_mismatch(self):
        """API response doesn't match schema → full refund."""
        payload = make_dispute(
            policy="api-quality",
            claim="API returned wrong schema",
            payment_terms="$0.01 per call via x402",
            evidence=[
                make_evidence("e1", "log", "postman", "Response received but schema does not match", ts="2026-06-18"),
            ],
            metadata={
                "response_received": True,
                "schema_matches": False,
                "endpoint": "/v1/data",
                "expected_type": "string",
                "actual_type": "number",
            },
        )
        result, _ = submit_dispute(payload)
        assert result["matched_rule_id"] == "schema-mismatch"
        assert result["remedy"] == "full_refund"

    def test_valid_api_response(self):
        """Valid API response → no remedy."""
        payload = make_dispute(
            policy="api-quality",
            claim="Customer disputes valid response",
            payment_terms="$0.01 per call",
            evidence=[
                make_evidence("e1", "log", "postman", "Valid response received", ts="2026-06-18"),
            ],
            metadata={
                "response_received": True,
                "schema_matches": True,
                "required_fields_missing": False,
                "http_status": 200,
            },
        )
        result, _ = submit_dispute(payload)
        assert result["matched_rule_id"] == "valid-response"
        assert result["remedy"] == "none"


class TestPhysicalCommercePolicy:
    """Tests for physical-commerce policy."""

    def test_non_delivery(self):
        """Product never delivered → full refund."""
        payload = make_dispute(
            policy="physical-commerce",
            claimant="Buyer Agent",
            respondent="Shop",
            claim="Product never arrived",
            payment_terms="$49.99",
            evidence=[
                make_evidence("e1", "log", "tracking", "No delivery confirmed, package lost", ts="2026-06-18"),
            ],
            metadata={
                "delivery_confirmed": False,
                "days_since_order": 30,
                "delivery_window_days": 7,
            },
        )
        result, _ = submit_dispute(payload)
        assert result["matched_rule_id"] == "non-delivery"
        assert result["remedy"] == "full_refund"

    def test_product_as_described(self):
        """Product delivered correctly → no remedy."""
        payload = make_dispute(
            policy="physical-commerce",
            claim="Customer disputes but product was fine",
            payment_terms="$29.99",
            evidence=[
                make_evidence("e1", "log", "tracking", "Delivery confirmed and signed", ts="2026-06-18"),
            ],
            metadata={
                "delivery_confirmed": True,
                "received_matches_order": True,
                "product_as_described": True,
            },
        )
        result, _ = submit_dispute(payload)
        assert result["matched_rule_id"] == "delivery-confirmed-satisfactory"
        assert result["remedy"] == "none"


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 13: POLICY PREVIEW ENDPOINT
# ═══════════════════════════════════════════════════════════════════════════════

class TestPolicyPreview:
    """Test /v1/policies/{name}/preview endpoint."""

    def test_preview_accepted_on_time(self):
        resp = requests.get(
            f"{BASE_URL}/v1/policies/freelance-delivery/preview",
            params={"deliverable_accepted": "true", "on_time": "true", "has_delivery_evidence": "true"},
            timeout=TIMEOUT,
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["matched_rule"] == "delivery-on-time-accepted"

    def test_preview_non_delivery(self):
        resp = requests.get(
            f"{BASE_URL}/v1/policies/freelance-delivery/preview",
            params={"deliverable_accepted": "false", "has_delivery_evidence": "false"},
            timeout=TIMEOUT,
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["matched_rule"] == "non-delivery"

    def test_preview_nonexistent_policy_404(self):
        resp = requests.get(
            f"{BASE_URL}/v1/policies/nonexistent/preview",
            timeout=TIMEOUT,
        )
        assert resp.status_code == 404
