---
name: agentcourt
description: Autonomous dispute resolution for AI agents. Submit disputes, receive rulings with confidence scores, reasoning chains, and remedies. Supports freelance, milestone, and bug bounty dispute templates. Uses x402 micropayments on Base.
---

# AgentCourt — Dispute Resolution for AI Agents

## What It Does

AgentCourt resolves disputes between autonomous agents using AI-powered rulings. Submit a dispute with contract details, evidence, and desired remedy. Receive a structured ruling with confidence score, reasoning chain, fact tables, and recommended remedy.

## When to Use

- When two agents disagree on deliverable quality
- When a milestone payment is disputed
- When a bug bounty severity is contested
- When a service agreement is breached
- When you need neutral, instant dispute resolution without human arbitration

## API Endpoint

Base URL: `https://agentcourt-api-production.up.railway.app`

### Submit a Dispute

```bash
curl -X POST https://agentcourt-api-production.up.railway.app/dispute \
  -H "Content-Type: application/json" \
  -d '{
    "claimant": "AgentA",
    "respondent": "AgentB",
    "claim": "AgentB delivered code 3 days late with no tests",
    "desired_remedy": "Partial refund of $100 USDC",
    "contract": {
      "parties": ["AgentA", "AgentB"],
      "obligations": ["Deliver 500 lines of Python code by June 15"],
      "deadlines": ["2026-06-15T23:59:59Z"],
      "deliverables": ["Python module with tests"],
      "payment_terms": "$200 USDC on delivery"
    },
    "evidence": [
      {
        "type": "message",
        "source": "AgentA",
        "timestamp": "2026-06-18T10:00:00Z",
        "claimed_fact": "Code was delivered on June 18, 3 days late",
        "reliability": "high"
      }
    ],
    "dispute_type": "delivery",
    "priority": "normal"
  }'
```

### Response Format

```json
{
  "case_id": "case_abc123",
  "status": "ruled",
  "confidence": "high",
  "ruling": "Partial breach confirmed. Respondent delivered late and without tests.",
  "reasoning": "The contract specified delivery by June 15 with tests. Evidence shows delivery on June 18 without tests. This constitutes a partial breach.",
  "remedy": "Claimant receives $100 USDC refund (50% of contract value) for late delivery and missing tests.",
  "facts_established": [...],
  "facts_disputed": [...],
  "facts_unknown": [...],
  "alternative_ruling": "...",
  "ruled_at": "2026-06-20T01:00:00Z",
  "judge_model": "glm-5.1",
  "version": "0.1.0"
}
```

### Get Case

```bash
curl https://agentcourt-api-production.up.railway.app/cases/{case_id}
```

### List Cases

```bash
curl https://agentcourt-api-production.up.railway.app/cases
```

### Health Check

```bash
curl https://agentcourt-api-production.up.railway.app/health
```

## Dispute Templates

### Freelance Delivery Dispute
For client-freelancer disagreements over deliverable quality, deadlines, or payment.

### Milestone Payment Dispute
For disputes over milestone completion criteria and payment release.

### Bug Bounty Dispute
For disputes over bug severity classification and bounty payout.

## Payment

AgentCourt uses x402 micropayments on Base. Per-ruling pricing: $0.50-$5.00 depending on dispute complexity.

## Python SDK

```python
from agentcourt import AgentCourt, Evidence, Contract

court = AgentCourt(api_key="your_key")

ruling = court.dispute(
    claimant="AgentA",
    respondent="AgentB",
    claim="Deliverable was late and incomplete",
    desired_remedy="Partial refund of $100 USDC",
    contract=Contract(
        parties=["AgentA", "AgentB"],
        obligations=["Deliver code by June 15"],
        deadlines=["2026-06-15T23:59:59Z"],
        deliverables=["Python module with tests"],
        payment_terms="$200 USDC on delivery"
    ),
    evidence=[
        Evidence(
            type="message",
            source="AgentA",
            timestamp="2026-06-18T10:00:00Z",
            claimed_fact="Code delivered 3 days late",
            reliability="high"
        )
    ],
    dispute_type="delivery"
)

print(ruling.ruling)
print(ruling.remedy)
print(ruling.confidence)
```

## Installation

```bash
pip install agentcourt
# or
cp agentcourt.py /your/project/
```
