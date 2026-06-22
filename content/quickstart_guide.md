# AgentCourt API — Quickstart Guide

**Live API:** `https://agentcourt-api-production.up.railway.app`
**Docs:** `https://agentcourt-api-production.up.railway.app/docs`
**OpenAPI:** `https://agentcourt-api-production.up.railway.app/openapi.json`

---

## 30-Second Quickstart

### Submit a dispute (cURL)
```bash
curl -X POST https://agentcourt-api-production.up.railway.app/v1/disputes \
  -H "Content-Type: application/json" \
  -d '{
    "claimant": "my_agent",
    "respondent": "freelancer_bot",
    "policy": "freelance-delivery",
    "claim": "Work never delivered",
    "desired_remedy": "full_refund",
    "contract": {
      "parties": ["my_agent", "freelancer_bot"],
      "obligations": ["Deliver logo design"],
      "deadlines": ["2026-06-20"]
    },
    "evidence": [
      {
        "type": "contract",
        "source": "agreement.pdf",
        "timestamp": "2026-06-01",
        "claimed_fact": "Logo due June 20"
      },
      {
        "type": "log",
        "source": "email.pdf",
        "timestamp": "2026-06-22",
        "claimed_fact": "No deliverable submitted"
      }
    ]
  }'
```

### Response
```json
{
  "case_id": "abc123",
  "status": "ruled",
  "matched_rule_id": "non-delivery",
  "remedy": "full_refund",
  "confidence": "high",
  "ruling": "The respondent failed to deliver...",
  "evidence_scores": [...]
}
```

---

## The Key Concept: `metadata`

For reliable rule matching, pass structured facts via the `metadata` field. The engine uses NLP extraction as a fallback, but explicit metadata always wins.

```json
{
  "policy": "sla-monitoring",
  "metadata": {
    "required_uptime": 99.9,
    "actual_uptime": 98.5,
    "max_latency": 200,
    "actual_latency": 450,
    "monitoring_period_confirmed": true
  }
}
```

---

## Python Quickstart
```python
import requests

API = "https://agentcourt-api-production.up.railway.app"

ruling = requests.post(f"{API}/v1/disputes", json={
    "claimant": "buyer_agent",
    "respondent": "api_provider",
    "policy": "api-quality",
    "claim": "API returned wrong data type",
    "desired_remedy": "full_refund",
    "contract": {
        "parties": ["buyer_agent", "api_provider"],
        "obligations": ["Match OpenAPI schema"],
        "deadlines": ["2026-06-22"]
    },
    "metadata": {
        "response_received": True,
        "schema_matches": False,
        "mismatched_field": "temperature",
        "expected_type": "integer",
        "actual_type": "string"
    },
    "evidence": [
        {"type": "contract", "source": "openapi.json",
         "timestamp": "2026-06-01", "claimed_fact": "temperature is integer"},
        {"type": "log", "source": "response.json",
         "timestamp": "2026-06-22", "claimed_fact": "temperature returned as string"}
    ]
}).json()

print(f"Ruling: {ruling['remedy']}")  # full_refund
print(f"Confidence: {ruling['confidence']}")  # medium
```

---

## JavaScript Quickstart
```javascript
const res = await fetch("https://agentcourt-api-production.up.railway.app/v1/disputes", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    claimant: "shopping_agent",
    respondent: "merchant",
    policy: "physical-commerce",
    claim: "Wrong product delivered",
    desired_remedy: "full_refund",
    contract: {
      parties: ["shopping_agent", "merchant"],
      obligations: ["Deliver correct product"],
      deadlines: ["2026-06-25"]
    },
    metadata: {
      delivery_confirmed: true,
      received_matches_order: false,
      ordered_product: "Blue sneakers size 10",
      received_product: "Red sneakers size 10"
    },
    evidence: [
      { type: "contract", source: "order", timestamp: "2026-06-20",
        claimed_fact: "Ordered blue sneakers" },
      { type: "log", source: "photo", timestamp: "2026-06-22",
        claimed_fact: "Received red sneakers" }
    ]
  })
});
const ruling = await res.json();
console.log(ruling.remedy); // full_refund
```

---

## Available Policy Templates

| Policy | Use Case | Key Metadata Fields |
|--------|----------|-------------------|
| `freelance-delivery` | Work-for-hire disputes | (NLP extraction works well) |
| `milestone-payment` | Staged deliverables | `milestone_completed`, `milestone_progress_pct`, `days_since_completion` |
| `bug-bounty` | Security bounty disputes | `bug_is_reproducible`, `actual_severity`, `severity_meets_threshold`, `disclosure_compliant` |
| `sla-monitoring` | Uptime/latency violations | `required_uptime`, `actual_uptime`, `max_latency`, `actual_latency` |
| `api-quality` | Paid API quality issues | `response_received`, `schema_matches`, `mismatched_field`, `http_status` |
| `physical-commerce` | Product purchase disputes | `delivery_confirmed`, `received_matches_order`, `shipping_damage` |

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Service health + loaded policies |
| `GET` | `/v1/policies` | List all policy templates |
| `GET` | `/v1/policies/{name}` | Get a specific template |
| `POST` | `/v1/disputes` | Submit a dispute for resolution |
| `GET` | `/v1/cases/{id}` | Look up a specific case |
| `GET` | `/v1/verdicts` | Browse all stored verdicts |

---

## Response Structure
```json
{
  "case_id": "unique-identifier",
  "status": "ruled",
  "matched_rule_id": "non-delivery",
  "policy_name": "freelance-delivery",
  "remedy": "full_refund",
  "confidence": "high",
  "ruling": "Human-readable ruling text...",
  "reasoning": "Matched policy rule 'non-delivery'...",
  "facts_established": [{"fact": "evidence_of_delivery", "value": "False"}],
  "facts_disputed": [...],
  "facts_unknown": [...],
  "evidence_scores": [{"id": "...", "type": "contract", "score": 0.777}],
  "ruled_at": "2026-06-22T17:31:58",
  "engine_version": "1.0.0"
}
```

**Confidence levels:** `high` (strong evidence match), `medium` (sufficient match), `low` (insufficient → escalates)

**Remedies:** `full_refund`, `partial_refund`, `full_payment_plus_penalty`, `service_credit`, `deny_payout`, `none`, `escalate`
