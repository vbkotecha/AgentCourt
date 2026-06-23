# AgentCourt Architecture

## Design Philosophy

AgentCourt is built on one core principle: **disputes should be resolved by rules, not opinions.**

When a transaction goes wrong, the relevant facts are usually deterministic:
- Was the response received? (boolean)
- Did it match the agreed schema? (boolean)
- Was the response time within SLA? (number comparison)
- Was delivery made by the deadline? (date comparison)

LLMs are great at nuanced judgment but terrible at consistency. The same evidence can produce different rulings on different runs. For commerce, consistency matters more than nuance.

## System Overview

```
                    ┌──────────────────┐
                    │   REST API       │
                    │  (FastAPI)       │
                    └──────┬───────────┘
                           │
                    ┌──────▼───────────┐
                    │  Policy Engine    │
                    │  (Rule Matcher)   │
                    └──────┬───────────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
     ┌────────▼───┐ ┌─────▼────┐ ┌────▼─────┐
     │  Policies  │ │ Evidence │ │ Contract │
     │  (7 types) │ │ Evaluator│ │  Matcher │
     └────────────┘ └──────────┘ └──────────┘
```

## Policy Engine

Each policy template is a JSON rule set:

```json
{
  "policy": "api-quality",
  "version": "1.2.0",
  "rules": [
    {
      "id": "AQ-001",
      "condition": "metadata.response_received == false",
      "ruling": "full_refund",
      "confidence": 0.95,
      "reasoning": "No response received from API"
    },
    {
      "id": "AQ-002",
      "condition": "metadata.response_received == true && metadata.schema_matches == false",
      "ruling": "full_refund",
      "confidence": 0.90,
      "reasoning": "Response schema does not match agreed format"
    }
  ]
}
```

### Rule Evaluation

Rules are evaluated in order. First match wins:

1. Evaluate each rule's condition against metadata + evidence
2. Return the first matching rule's ruling
3. If no rules match, default ruling with low confidence (escalation candidate)

### Determinism Guarantee

Same `policy + metadata + evidence` ALWAYS produces the same `ruling + confidence`.
This is enforced by design — no random components, no LLM calls, no external state.

## Evidence Model

```json
{
  "type": "log|screenshot|test|contract|transaction|other",
  "source": "string (origin of evidence)",
  "timestamp": "ISO 8601",
  "claimed_fact": "string (what this evidence shows)",
  "hash": "optional content hash for integrity"
}
```

Evidence is evaluated structurally, not interpreted semantically.

## API Flow

```
1. POST /v1/disputes
   → Parse dispute payload
   → Load policy template
   → Evaluate rules against metadata + evidence
   → Generate case_id
   → Return ruling + confidence + reasoning

2. GET /v1/cases/{case_id}
   → Retrieve stored case with full audit trail

3. GET /v1/policies
   → List all available policies with rule counts
```

## Non-Custodial Design

AgentCourt never holds funds. This is a deliberate architectural choice:

- **No financial regulation**: Not a money transmitter
- **No custody risk**: Nothing to steal
- **No lockup**: Transactions settle immediately
- **Enforcement via consequence**: Rulings adjust reputation, inform marketplaces, create precedent

When escrow is needed (high-value transactions), AgentCourt rulings can be consumed by escrow systems (like Arbitova) to trigger fund release or refund.

## x402 Integration

AgentCourt is x402-native:

```json
// /.well-known/x402
{
  "name": "AgentCourt",
  "network": "base-mainnet",
  "currency": "USDC",
  "payTo": "0x9863aB6242663FCc84c33632741711dB78f8Fd15",
  "endpoints": [{"path": "/v1/disputes", "price": "$0.05"}],
  "free_tier": {"requests_per_month": 100}
}
```

Free tier (100 disputes/month) requires no payment. Paid disputes cost $0.05 in USDC on Base.

## Extensibility

New policies can be added without code changes — just add a policy JSON file:

```bash
# Add a new "data-licensing" policy
cp src/engine/policies/api-quality.json src/engine/policies/data-licensing.json
# Edit rules, restart server
```

This enables community-contributed policies via PR.
