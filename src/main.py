import os
from pathlib import Path

# Load .env file
env_file = Path(__file__).parent.parent / ".env"
if env_file.exists():
    for line in env_file.read_text().strip().splitlines():
        if "=" in line and not line.startswith("#"):
            key, val = line.split("=", 1)
            os.environ.setdefault(key.strip(), val.strip())

"""
AgentCourt v1 — Policy-Driven Dispute Resolution API
"""

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import uuid
import json
import sys

# Add src to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from engine.policy_engine import (
    evaluate_dispute,
    load_policy,
    list_policies,
    score_evidence,
    extract_facts,
    evaluate_rules,
    generate_ruling,
    calculate_confidence,
)

app = FastAPI(
    title="AgentCourt",
    version="1.0.0",
    description="Policy-driven dispute resolution protocol for agent commerce",
)

# --- Data directory ---
DATA_DIR = os.environ.get("AGENTCOURT_DATA_DIR", "/root/.letta/agentcourt/data")
os.makedirs(DATA_DIR, exist_ok=True)


# ─── Schemas ─────────────────────────────────────────────────────────────────

class EvidenceItem(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:12])
    type: str  # contract, message, payment, file, log, screenshot, commit, other
    source: str
    timestamp: str
    content_hash: Optional[str] = None
    content_uri: Optional[str] = None
    claimed_fact: str
    excerpt: Optional[str] = None
    reliability: Optional[str] = None  # high / medium / low
    notes: Optional[str] = None


class ContractTerms(BaseModel):
    parties: List[str]
    obligations: List[str]
    deadlines: Optional[List[str]] = None
    deliverables: Optional[List[str]] = None
    payment_terms: Optional[str] = None
    definitions: Optional[dict] = None
    raw_contract: Optional[str] = None


class DisputeRequest(BaseModel):
    case_id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4())[:12])
    claimant: str
    respondent: str
    contract: ContractTerms
    claim: str
    desired_remedy: str
    evidence: List[EvidenceItem]
    policy: str = "freelance-delivery"  # which policy template to use
    dispute_type: Optional[str] = None
    priority: Optional[str] = "normal"
    metadata: Optional[dict] = None  # for policy-specific facts (progress_pct, severity, etc.)


class RulingResponse(BaseModel):
    case_id: str
    status: str
    confidence: str
    ruling: str
    reasoning: str
    remedy: str
    facts_established: List[dict]
    facts_disputed: List[dict]
    facts_unknown: List[dict]
    matched_rule_id: Optional[str] = None
    policy_name: Optional[str] = None
    policy_version: Optional[str] = None
    evidence_scores: Optional[List[dict]] = None
    ruled_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    engine_version: str = "1.0.0"


# ─── Storage ─────────────────────────────────────────────────────────────────

def save_case(case_id: str, data: dict):
    path = os.path.join(DATA_DIR, f"{case_id}.json")
    with open(path, "w") as f:
        json.dump(data, f, indent=2, default=str)


def load_case(case_id: str) -> Optional[dict]:
    path = os.path.join(DATA_DIR, f"{case_id}.json")
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return None


def list_cases(limit: int = 50) -> List[dict]:
    cases = []
    for fname in os.listdir(DATA_DIR):
        if fname.endswith(".json"):
            with open(os.path.join(DATA_DIR, fname)) as f:
                cases.append(json.load(f))
    return sorted(cases, key=lambda c: c.get("request", {}).get("created_at", ""), reverse=True)[:limit]


# ─── API Endpoints ───────────────────────────────────────────────────────────

@app.post("/v1/disputes", response_model=RulingResponse)
async def create_dispute(dispute: DisputeRequest):
    """Submit a dispute and receive a policy-driven ruling."""
    # Convert to dict for the engine
    dispute_dict = dispute.model_dump()

    # Save the case
    case_data = {
        "case_id": dispute.case_id,
        "claimant": dispute.claimant,
        "respondent": dispute.respondent,
        "claim": dispute.claim,
        "policy": dispute.policy,
        "dispute_type": dispute.dispute_type,
        "evidence_count": len(dispute.evidence),
        "created_at": datetime.utcnow().isoformat(),
        "status": "pending",
    }
    save_case(dispute.case_id, {"request": case_data})

    # Evaluate the dispute through the policy engine
    try:
        ruling = evaluate_dispute(
            dispute=dispute_dict,
            evidence=[e.model_dump() for e in dispute.evidence],
            policy_name=dispute.policy,
        )
    except FileNotFoundError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Engine error: {str(e)}")

    # Save the ruling
    case_data["status"] = ruling["status"]
    case_data["ruling"] = ruling
    save_case(dispute.case_id, {"request": case_data, "ruling": ruling})

    return RulingResponse(
        case_id=ruling["case_id"],
        status=ruling["status"],
        confidence=ruling["confidence"],
        ruling=ruling["ruling"],
        reasoning=ruling["reasoning"],
        remedy=ruling["remedy"],
        facts_established=ruling["facts_established"],
        facts_disputed=ruling["facts_disputed"],
        facts_unknown=ruling["facts_unknown"],
        matched_rule_id=ruling.get("matched_rule_id"),
        policy_name=ruling.get("policy_name"),
        policy_version=ruling.get("policy_version"),
        evidence_scores=ruling.get("evidence_scores"),
        ruled_at=ruling["ruled_at"],
        engine_version=ruling["engine_version"],
    )


@app.get("/v1/cases")
async def get_cases(limit: int = Query(50, ge=1, le=200)):
    """List all cases."""
    return list_cases(limit)


@app.get("/v1/cases/{case_id}")
async def get_case(case_id: str):
    """Get a specific case with its ruling."""
    case = load_case(case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return case


@app.get("/v1/policies")
async def get_policies():
    """List all available policy templates."""
    return list_policies()


@app.get("/v1/policies/{policy_name}")
async def get_policy(policy_name: str):
    """Get details of a specific policy template."""
    try:
        return load_policy(policy_name)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Policy '{policy_name}' not found")


@app.get("/v1/policies/{policy_name}/preview")
async def preview_policy_evaluation(
    policy_name: str,
    # Sample facts as query params for quick testing
    deliverable_accepted: Optional[str] = Query(None, description="true/false/null"),
    on_time: Optional[str] = Query(None, description="true/false"),
    has_delivery_evidence: Optional[str] = Query(None, description="true/false"),
):
    """Preview which rule would match given hypothetical facts."""
    try:
        policy = load_policy(policy_name)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Policy '{policy_name}' not found")

    facts = {}
    if deliverable_accepted is not None:
        facts["deliverable_was_accepted"] = deliverable_accepted == "true" if deliverable_accepted != "null" else None
    if on_time is not None:
        facts["delivery_was_on_time"] = on_time == "true"
    if has_delivery_evidence is not None:
        facts["evidence_of_delivery"] = has_delivery_evidence == "true"

    matched = evaluate_rules(policy, facts)
    return {
        "policy": policy_name,
        "input_facts": facts,
        "matched_rule": matched.get("id"),
        "would_ruling": matched.get("ruling_template"),
        "predicted_confidence": matched.get("confidence"),
        "predicted_remedy": matched.get("remedy"),
    }


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "version": "1.0.0",
        "data_dir": DATA_DIR,
        "engine": "policy-engine-v1",
        "policies": [p["name"] for p in list_policies()],
    }
