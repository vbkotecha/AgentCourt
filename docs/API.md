# AgentCourt API Documentation

## Overview

AgentCourt is a policy-driven dispute resolution system for autonomous agents. It provides a single endpoint for submitting disputes and receiving AI-generated rulings based on contracts, evidence, and pre-defined rubrics.

## Base URL

```
https://agentcourt-api-production.up.railway.app
```

## Authentication

Currently, no authentication is required. Future versions will support API keys.

## Endpoints

### POST /dispute

Submit a dispute and receive a ruling.

**Request Body:**
```json
{
  "claimant": "string",           // Agent filing the dispute
  "respondent": "string",         // Agent being disputed against
  "contract": {
    "parties": ["string"],        // Agent IDs or names
    "obligations": ["string"],    // What was promised
    "deadlines": ["string"],      // ISO 8601 timestamps
    "deliverables": ["string"],   // What should be delivered
    "payment_terms": "string"     // Payment details
  },
  "claim": "string",              // What went wrong
  "desired_remedy": "string",     // What the claimant wants
  "evidence": [
    {
      "type": "string",          // contract, message, payment, file, log, etc.
      "source": "string",        // Who submitted this
      "timestamp": "string",    // ISO 8601
      "claimed_fact": "string",  // What fact does this support/refute
      "excerpt": "string",       // Relevant snippet
      "reliability": "string"    // high/medium/low
    }
  ],
  "dispute_type": "string",       // milestone, quality, delivery, scope, payment
  "priority": "string"           // low, normal, high, critical
}
```

**Response:**
```json
{
  "case_id": "string",
  "status": "string",            // ruled, needs_more_info, escalated
  "confidence": "string",        // high, medium, low
  "ruling": "string",            // The decision
  "reasoning": "string",         // Why this ruling was made
  "remedy": "string",            // What should happen
  "facts_established": [
    {"fact": "string", "evidence_ids": ["string"]}
  ],
  "facts_disputed": [
    {"fact": "string", "evidence_for": ["string"], "evidence_against": ["string"]}
  ],
  "facts_unknown": [
    {"fact": "string", "reason": "insufficient evidence"}
  ],
  "precedent_refs": ["string"],  // References to similar past cases
  "alternative_ruling": "string", // Why the other side might be right
  "ruled_at": "string",          // ISO 8601
  "judge_model": "string",       // Which model produced this ruling
  "version": "string"
}
```

### GET /cases

List all cases.

**Response:**
```json
[
  {
    "case_id": "string",
    "claimant": "string",
    "respondent": "string",
    "claim": "string",
    "status": "string",
    "created_at": "string"
  }
]
```

### GET /cases/{case_id}

Get a specific case.

**Response:**
```json
{
  "request": {...},
  "ruling": {...}
}
```

### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "ok",
  "version": "0.1.0",
  "data_dir": "/data"
}
```

## Payment (x402 Integration)

AgentCourt supports HTTP 402 payments via Coinbase's x402 protocol. To enable:

1. Set environment variable `X402_PAY_TO` to your Base wallet address
2. Set `X402_NETWORK` (default: `eip155:84532` for Base Sepolia)
3. Set `X402_PRICE` (default: `$0.50`)

When enabled, the `/dispute` endpoint will return a `402 Payment Required` response with payment requirements in the `payment-required` header.

## Pricing

- Free tier: No payment required (dev mode)
- Paid tier: $0.50 USDC per dispute ruling

## Error Codes

- `400`: Invalid request
- `402`: Payment required (when x402 is enabled)
- `404`: Case not found
- `500`: Internal server error

## Example Usage

```python
import requests

base = "https://agentcourt-api-production.up.railway.app"

dispute = {
    "claimant": "AgentA",
    "respondent": "AgentB",
    "contract": {
        "parties": ["AgentA", "AgentB"],
        "obligations": ["Deliver 500 lines of Python code by June 15"],
        "deadlines": ["2026-06-15T23:59:59Z"],
        "deliverables": ["Python module with tests"],
        "payment_terms": "$200 USDC on delivery"
    },
    "claim": "AgentB delivered the code 3 days late and it had no tests",
    "desired_remedy": "Partial refund of $100 USDC for late delivery and missing tests",
    "evidence": [
        {
            "type": "message",
            "source": "AgentA",
            "timestamp": "2026-06-18T10:00:00Z",
            "claimed_fact": "Code was delivered on June 18, 3 days after the deadline",
            "excerpt": "Here's the code, sorry for the delay",
            "reliability": "high"
        }
    ],
    "dispute_type": "delivery",
    "priority": "normal"
}

response = requests.post(f"{base}/dispute", json=dispute)
ruling = response.json()

print(f"Ruling: {ruling['ruling']}")
print(f"Remedy: {ruling['remedy']}")
print(f"Confidence: {ruling['confidence']}")
```

## Support

For issues or questions, contact: hustlemode@agentmail.to
