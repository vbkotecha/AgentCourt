# AgentCourt × Agentic.market Integration Pitch

## The Problem

Agentic.market processes 165M+ transactions across 480,000+ agents. When an agent pays for inference from OpenAI and gets degraded output, or pays for data from Bloomberg and receives stale data, or contracts for cloud infrastructure from AWS Lambda and the SLA is breached — what happens?

Right now: nothing. The x402 protocol handles payment authorization. It doesn't handle disputes.

## The Solution

AgentCourt sits as a dispute resolution layer between Agentic.market's payment flow and its trust/identity system:

```
Agent A requests service → x402 payment → Service delivered
         ↓ (if dispute)
    AgentCourt dispute resolution → ruling → enforcement
```

## Integration: 3 API Calls

```python
# 1. When a transaction is disputed
ruling = court.dispute(
    claimant="agent_buyer",
    respondent="agent_seller",
    contract={
        "obligations": ["Provide inference API with 200ms max latency"],
        "payment_terms": "0.01 USDC per request"
    },
    claim="Inference latency exceeded 500ms consistently",
    policy="sla-monitoring",
    evidence=[
        {"type": "log", "source": "latency_monitor",
         "claimed_fact": f"Average latency {avg_ms}ms vs 200ms guaranteed"},
        {"type": "log", "source": "x402_receipt",
         "claimed_fact": f"Payment of {amount} USDC made for {n} requests"}
    ]
)

# 2. Ruling returns
# ruling.matched_rule → "latency-breach"
# ruling.remedy → "service_credit"
# ruling.confidence → "medium"

# 3. Agentic.market enforces
if ruling.remedy == "service_credit":
    issue_refund(buyer, credit_amount)
    log_to_agent_trust_score(seller, breach=True)
```

## Why AgentCourt (not a custom solution)

1. **Built for agents, not humans** — evidence is machine-readable, not PDFs
2. **Policy-first** — define rules once, all disputes follow them
3. **Deterministic** — same evidence always produces the same ruling
4. **Evidence-native** — content hashing, provenance, chain of custody
5. **API-first** — 3 calls to integrate, no infrastructure to manage
6. **4 policy templates ready** — SLA monitoring, freelance delivery, milestone payment, bug bounty

## Stats

- 17/17 test cases passing across all policy templates
- 21 public verdicts on the dashboard
- OpenAPI spec, Swagger UI, Python SDK, JS SDK, MCP server all ready
- Average ruling time: <500ms per dispute
