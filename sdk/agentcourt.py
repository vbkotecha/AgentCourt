"""
AgentCourt Python SDK — Dispute resolution for autonomous agents.

Usage:
    from agentcourt import AgentCourt

    court = AgentCourt(api_key="your_key")  # or set AGENTCOURT_API_KEY env var

    # Submit a dispute
    ruling = court.dispute(
        claimant="AgentA",
        respondent="AgentB",
        claim="AgentB delivered code 3 days late with no tests",
        contract={
            "parties": ["AgentA", "AgentB"],
            "obligations": ["Deliver 500 lines of Python code by June 15"],
            "deadlines": ["2026-06-15T23:59:59Z"],
            "deliverables": ["Python module with tests"],
            "payment_terms": "$200 USDC on delivery"
        },
        desired_remedy="Partial refund of $100 USDC for late delivery and missing tests",
        evidence=[
            {
                "type": "message",
                "source": "AgentA",
                "timestamp": "2026-06-18T10:00:00Z",
                "claimed_fact": "Code was delivered on June 18, 3 days after the deadline",
                "excerpt": "Here's the code, sorry for the delay",
                "reliability": "high"
            }
        ],
        dispute_type="delivery",
        priority="normal"
    )

    print(ruling.case_id)
    print(ruling.ruling)
    print(ruling.remedy)
    print(ruling.confidence)
"""

import os
import json
import urllib.request
import urllib.error
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any


BASE_URL = "https://agentcourt-api-production.up.railway.app"
DEFAULT_API_KEY_ENV = "AGENTCOURT_API_KEY"


@dataclass
class Evidence:
    """Evidence item for a dispute."""
    type: str  # contract, message, payment, file, log, etc.
    source: str  # Who submitted this
    timestamp: str  # ISO 8601
    claimed_fact: str  # What fact does this support/refute
    excerpt: str = ""  # Relevant snippet
    reliability: str = "medium"  # high, medium, low


@dataclass
class Contract:
    """Contract details for a dispute."""
    parties: List[str]
    obligations: List[str]
    deadlines: List[str] = field(default_factory=list)
    deliverables: List[str] = field(default_factory=list)
    payment_terms: str = ""


@dataclass
class Ruling:
    """Ruling returned by AgentCourt."""
    case_id: str
    status: str
    confidence: str
    ruling: str
    reasoning: str
    remedy: str
    facts_established: List[Dict[str, Any]] = field(default_factory=list)
    facts_disputed: List[Dict[str, Any]] = field(default_factory=list)
    facts_unknown: List[Dict[str, Any]] = field(default_factory=list)
    precedent_refs: List[str] = field(default_factory=list)
    alternative_ruling: str = ""
    ruled_at: str = ""
    judge_model: str = ""
    version: str = ""
    raw: Dict[str, Any] = field(default_factory=dict)


class AgentCourtError(Exception):
    """Error from the AgentCourt API."""
    def __init__(self, message: str, status_code: int = 0, details: Dict = None):
        super().__init__(message)
        self.status_code = status_code
        self.details = details or {}


class AgentCourt:
    """AgentCourt SDK — Dispute resolution for autonomous agents."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = BASE_URL,
        timeout: int = 60,
    ):
        self.api_key = api_key or os.environ.get(DEFAULT_API_KEY_ENV, "")
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def _request(
        self,
        method: str,
        path: str,
        data: Optional[Dict] = None,
    ) -> Dict:
        url = f"{self.base_url}{path}"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "agentcourt-sdk/0.1.0",
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        body = json.dumps(data).encode() if data else None
        req = urllib.request.Request(url, data=body, method=method, headers=headers)

        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            error_body = e.read().decode()
            try:
                error_data = json.loads(error_body)
            except json.JSONDecodeError:
                error_data = {"error": error_body}
            raise AgentCourtError(
                message=error_data.get("error", {}).get("message", error_body),
                status_code=e.code,
                details=error_data,
            )

    def dispute(
        self,
        claimant: str,
        respondent: str,
        claim: str,
        desired_remedy: str,
        contract: Optional[Contract] = None,
        evidence: Optional[List[Evidence]] = None,
        dispute_type: str = "general",
        priority: str = "normal",
    ) -> Ruling:
        """Submit a dispute and receive a ruling."""
        payload: Dict[str, Any] = {
            "claimant": claimant,
            "respondent": respondent,
            "claim": claim,
            "desired_remedy": desired_remedy,
            "dispute_type": dispute_type,
            "priority": priority,
        }

        if contract:
            payload["contract"] = {
                "parties": contract.parties,
                "obligations": contract.obligations,
                "deadlines": contract.deadlines,
                "deliverables": contract.deliverables,
                "payment_terms": contract.payment_terms,
            }

        if evidence:
            payload["evidence"] = [
                {
                    "type": e.type,
                    "source": e.source,
                    "timestamp": e.timestamp,
                    "claimed_fact": e.claimed_fact,
                    "excerpt": e.excerpt,
                    "reliability": e.reliability,
                }
                for e in evidence
            ]

        result = self._request("POST", "/dispute", data=payload)
        return Ruling(
            case_id=result.get("case_id", ""),
            status=result.get("status", ""),
            confidence=result.get("confidence", ""),
            ruling=result.get("ruling", ""),
            reasoning=result.get("reasoning", ""),
            remedy=result.get("remedy", ""),
            facts_established=result.get("facts_established", []),
            facts_disputed=result.get("facts_disputed", []),
            facts_unknown=result.get("facts_unknown", []),
            precedent_refs=result.get("precedent_refs", []),
            alternative_ruling=result.get("alternative_ruling", ""),
            ruled_at=result.get("ruled_at", ""),
            judge_model=result.get("judge_model", ""),
            version=result.get("version", ""),
            raw=result,
        )

    def get_case(self, case_id: str) -> Dict:
        """Get a specific case by ID."""
        return self._request("GET", f"/cases/{case_id}")

    def list_cases(self) -> List[Dict]:
        """List all cases."""
        result = self._request("GET", "/cases")
        return result if isinstance(result, list) else result.get("data", [])

    def health(self) -> Dict:
        """Check API health."""
        return self._request("GET", "/health")
