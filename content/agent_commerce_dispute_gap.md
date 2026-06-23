# The Missing Layer in Agent Commerce: Dispute Resolution (And Why We Open-Sourced It)

The agent commerce stack is nearly complete. AWS AgentCore Payments went live in May. Stripe has agent checkout. x402 lets agents pay per API call in USDC. Visa, Mastercard, and AmEx all shipped agent payment protocols in Q2 2026.

Payments work. What doesn't work is what happens when they go wrong.

## The Problem

When a human buys something online and it goes wrong, they file a chargeback. The credit card network has a 50-year-old dispute infrastructure: evidence, arbitration, reversal.

When an agent pays another agent via x402 and gets the wrong data? There's no chargeback button. No phone number. No dispute form. Just a failed transaction and no recourse.

The dispute rate for agent-initiated transactions is **2.4x higher** than human-initiated transactions (TrustSphere, April 2026). And FraudBeat noted in May 2026: "dispute management does not appear in agentic commerce reports."

Everyone built the payment rail. Nobody built the dispute resolution layer.

## What We Built

**AgentCourt** is an open-source, policy-driven dispute resolution API. It's live, MIT-licensed, and x402-native.

### How It Works

1. **Define policies** — Each transaction type has a policy template with deterministic rules. Freelance delivery has rules for non-delivery, late delivery, partial delivery. Bug bounty has rules for reproducibility, severity, disclosure compliance.

2. **Submit disputes** — When something goes wrong, submit evidence + structured facts. The API evaluates against the policy rules and returns a ruling in under 500ms.

3. **Get deterministic rulings** — No LLM guessing. Rules match conditions like `deliverable_was_accepted == false AND evidence_of_delivery == false` → `non-delivery` → `full_refund`. Every ruling is traceable to a specific rule + evidence.

### What Makes It Different

| Feature | AgentCourt | Traditional Chargebacks | AgentLair | Rivero/Amiko |
|---------|-----------|------------------------|-----------|--------------|
| Speed | <500ms | 30-90 days | Manual review | 24/7 AI assist |
| Cost | $0.05/dispute | $15-25/case | Free demo | Enterprise SaaS |
| Open Source | MIT | No | No | No |
| x402-native | Yes | No | Partial | No |
| Non-custodial | Yes | N/A | Yes | No |
| Deterministic | Yes | No | No | No |

### Live Example

```bash
curl -X POST https://agentcourt-api-production.up.railway.app/v1/disputes \
  -H "Content-Type: application/json" \
  -d '{
    "policy": "api-quality",
    "claim": "API returned integer instead of string",
    "claimant": "consumer_agent",
    "respondent": "data_provider",
    "desired_remedy": "full_refund",
    "contract": {"parties": ["consumer_agent", "data_provider"], "obligations": ["Match OpenAPI schema"]},
    "metadata": {"response_received": true, "schema_matches": false},
    "evidence": [{"type": "log", "source": "response.json", "timestamp": "2026-06-22", "claimed_fact": "Expected string, got int"}]
  }'
```

Response:
```json
{
  "matched_rule_id": "schema-mismatch",
  "remedy": "full_refund",
  "confidence": "high",
  "processing_time_ms": 14
}
```

14 milliseconds. Not 14 business days.

## Why We Didn't Build Escrow

Escrow is the obvious answer for disputes — hold funds until both parties are satisfied. We deliberately didn't build it.

**Escrow = financial regulation = kills velocity.**

Most agent disputes aren't about money custody. They're about: Did the API match its schema? Was the deliverable on time? Was the bug reproducible? Did the agent exceed its mandate?

The ruling matters through **consequence** — reputation scores, precedent, marketplace enforcement — not through holding money hostage. AgentCourt produces rulings. Marketplaces enforce them.

Escrow can come later, for high-value disputes, when users demand it.

## The 7 Policy Templates

Every policy is a JSON file with deterministic rules. Here are the live ones:

1. **freelance-delivery** — non-delivery, late delivery, partial delivery, on-time
2. **milestone-payment** — completed-unpaid, overdue (with penalty), incomplete
3. **bug-bounty** — full payout (critical), partial severity, not reproducible
4. **sla-monitoring** — uptime violation, latency breach, partial degradation
5. **api-quality** — schema mismatch, empty response, wrong data type, stale data
6. **physical-commerce** — non-delivery, wrong product, damaged, return disputes
7. **scope-dispute** — agent mandate exceeded, budget exceeded, ambiguous mandate

## What's Next

- **ERC-8183 alignment** — AgentCourt IS the "Evaluator" role in the ERC-8183 spec
- **ADRP compatibility** — Layers 1-3 of IETF draft-stone-adrp-00
- **Reputation & precedent system** — Rulings create case law. Repeat offenders get flagged.
- **Marketplace integration** — API + SDKs + webhooks for platforms to enforce rulings
- **Appeal + human fallback** — When machine confidence is low, escalate to human arbitration

## Links

- **Live API**: https://agentcourt-api-production.up.railway.app/docs
- **GitHub**: https://github.com/vbkotecha/agentcourt-api
- **License**: MIT
- **Self-host**: `docker-compose up`
- **SDKs**: Python, JavaScript, TypeScript (zero-dependency)

The agent commerce stack needed a dispute layer. Now it has one.
