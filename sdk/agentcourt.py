"""
AgentCourt SDK — Submit disputes and get rulings programmatically.
Zero dependencies. Uses standard library only.

Usage:
    from agentcourt import AgentCourt
    
    court = AgentCourt()
    
    ruling = court.dispute(
        claimant="ClientCorp",
        respondent="DevStudio",
        contract={"obligations": ["Build app"], "deadlines": ["2026-07-01T23:59:00Z"]},
        claim="No delivery",
        desired_remedy="Refund",
        policy="freelance-delivery",
        evidence=[
            {"type": "contract", "source": "ClientCorp", "timestamp": "2026-06-01T10:00:00Z",
             "claimed_fact": "No deliverable received", "reliability": "high"}
        ]
    )
    
    print(ruling.confidence)  # HIGH
    print(ruling.remedy)      # full_refund
"""

import json
import urllib.request
import urllib.error
from typing import Optional, List
from dataclasses import dataclass


@dataclass
class Ruling:
    case_id: str
    status: str
    confidence: str
    ruling: str
    reasoning: str
    remedy: str
    facts_established: list
    facts_unknown: list
    matched_rule_id: Optional[str]
    policy_name: Optional[str]
    evidence_scores: list
    ruled_at: str
    
    @property
    def is_high_confidence(self) -> bool:
        return self.confidence == "high"
    
    @property
    def is_ruled(self) -> bool:
        return self.status == "ruled"


class AgentCourt:
    """AgentCourt dispute resolution client. Zero dependencies."""
    
    def __init__(self, base_url: str = "https://agentcourt-api-production.up.railway.app"):
        self.base_url = base_url.rstrip("/")
    
    def _post(self, path: str, data: dict) -> dict:
        payload = json.dumps(data).encode()
        req = urllib.request.Request(
            f"{self.base_url}{path}",
            data=payload,
            method="POST",
            headers={"Content-Type": "application/json"},
        )
        try:
            resp = urllib.request.urlopen(req, timeout=30)
            return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            body = e.read().decode()
            raise Exception(f"API error {e.code}: {body}") from e
    
    def _get(self, path: str) -> dict:
        req = urllib.request.Request(f"{self.base_url}{path}")
        try:
            resp = urllib.request.urlopen(req, timeout=30)
            return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            body = e.read().decode()
            raise Exception(f"API error {e.code}: {body}") from e
    
    def dispute(
        self,
        claimant: str,
        respondent: str,
        contract: dict,
        claim: str,
        desired_remedy: str,
        policy: str = "freelance-delivery",
        evidence: List[dict] = None,
        metadata: dict = None,
    ) -> Ruling:
        """Submit a dispute and get a ruling."""
        payload = {
            "claimant": claimant,
            "respondent": respondent,
            "contract": contract,
            "claim": claim,
            "desired_remedy": desired_remedy,
            "policy": policy,
            "evidence": evidence or [],
            "metadata": metadata or {},
        }
        
        data = self._post("/v1/disputes", payload)
        
        return Ruling(
            case_id=data["case_id"],
            status=data["status"],
            confidence=data["confidence"],
            ruling=data["ruling"],
            reasoning=data.get("reasoning", ""),
            remedy=data["remedy"],
            facts_established=data.get("facts_established", []),
            facts_unknown=data.get("facts_unknown", []),
            matched_rule_id=data.get("matched_rule_id"),
            policy_name=data.get("policy_name"),
            evidence_scores=data.get("evidence_scores", []),
            ruled_at=data.get("ruled_at", ""),
        )
    
    def get_case(self, case_id: str) -> dict:
        """Retrieve a case by ID."""
        return self._get(f"/v1/cases/{case_id}")
    
    def list_policies(self) -> list:
        """List available policy templates."""
        return self._get("/v1/policies")
    
    def health(self) -> dict:
        """Check API health."""
        return self._get("/health")


def dispute(**kwargs) -> Ruling:
    """Quick submit without creating a client."""
    return AgentCourt().dispute(**kwargs)


if __name__ == "__main__":
    print("=== AgentCourt SDK Demo ===\n")
    
    court = AgentCourt()
    
    policies = court.list_policies()
    print(f"Policies: {[p['name'] for p in policies]}")
    
    ruling = court.dispute(
        claimant="Acme Corp",
        respondent="Freelancer X",
        contract={
            "parties": ["Acme Corp", "Freelancer X"],
            "obligations": ["Build dashboard"],
            "deadlines": ["2026-06-15T23:59:00Z"],
            "deliverables": ["React dashboard"],
        },
        claim="Freelancer never delivered the dashboard",
        desired_remedy="Full refund",
        policy="freelance-delivery",
        evidence=[
            {
                "type": "contract",
                "source": "Acme Corp",
                "timestamp": "2026-06-01T10:00:00Z",
                "claimed_fact": "No deliverable received",
                "reliability": "high",
                "content_hash": "sha256:demo123",
            }
        ],
    )
    
    print(f"\nCase: {ruling.case_id}")
    print(f"Status: {ruling.status}")
    print(f"Confidence: {ruling.confidence}")
    print(f"Rule: {ruling.matched_rule_id}")
    print(f"Remedy: {ruling.remedy}")
    print(f"Ruling: {ruling.ruling}")
