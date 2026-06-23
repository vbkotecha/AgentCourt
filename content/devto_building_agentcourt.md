---
title: "Building AgentCourt: Dispute Resolution for the Agent Economy"
published: false
description: "When AI agents transact autonomously and things go wrong, who resolves it? Here's how we built a deterministic dispute resolution API."
tags: aiagents, api, web3, opensource
cover_image: https://vbkotecha.github.io/agentcourt-api/og-image.png
---

## The Missing Layer in Agent Commerce

The AI agent stack is evolving fast:

1. **Communication**: A2A protocol, MCP (how agents talk)
2. **Payment**: x402, USDC on Base (how agents pay)
3. **Discovery**: CDP Bazaar, agent directories (how agents find each other)

But there's a fourth layer that nobody talks about:

4. **Dispute resolution** — what happens when the transaction goes wrong?

When an agent pays for an API call and gets XML instead of JSON... when a freelance agent delivers partial work... when an SLA is breached... **who decides what's fair?**

That's the problem AgentCourt solves.

## Why Not Use LLMs for Dispute Resolution?

We considered using an LLM to evaluate disputes. It's tempting — just feed the evidence to GPT-4 and ask for a ruling.

But there's a fundamental problem: **LLMs are non-deterministic.**

Same dispute → different ruling → depending on temperature, context window, or model version. For financial decisions, that's unacceptable.

Instead, AgentCourt uses **deterministic policy templates**:

```json
{
  "policy": "api-quality",
  "claim": "API returned XML instead of JSON",
  "metadata": {
    "response_received": true,
    "schema_matches": false
  }
}
```

The API evaluates the metadata against 7 rules and returns a ruling:

```json
{
  "ruling": "full_refund",
  "confidence": "0.90",
  "matched_rule": "api-schema-mismatch",
  "case_id": "case-a1b2c3"
}
```

Same input → same output. Every time. That's the foundation for trust.

## The Architecture

AgentCourt is intentionally simple:

- **FastAPI** backend (Python)
- **Pydantic** models for input validation
- **JSON policy templates** for rule evaluation
- **x402** middleware for micropayments ($0.05/dispute)
- **No database** — stateless, each dispute is evaluated independently

This gives us:
- **<500ms latency** — fast enough to block a bad transaction
- **Zero hallucination risk** — no LLM in the ruling path
- **Full auditability** — every ruling includes the matched rule ID

## Seven Policy Templates

| Policy | Use Case | Rules |
|--------|----------|-------|
| `api-quality` | Schema mismatch, empty response | 7 |
| `freelance-delivery` | Non-delivery, late delivery | 6 |
| `milestone-payment` | Unpaid milestones | 5 |
| `bug-bounty` | Severity disputes | 5 |
| `sla-monitoring` | Uptime violations | 5 |
| `scope-dispute` | Budget exceedance | 5 |
| `physical-commerce` | Damaged goods | 6 |

Each policy is a JSON file that defines rules, thresholds, and remedies. Anyone can contribute new policies via PR.

## Integration in 30 Seconds

```bash
curl -X POST https://agentcourt-api-production.up.railway.app/v1/disputes \
  -H "Content-Type: application/json" \
  -d '{
    "policy": "api-quality",
    "claim": "API returned XML instead of JSON",
    "desired_remedy": "full_refund",
    "metadata": {"response_received": true, "schema_matches": false}
  }'
```

Or use the SDK:

```python
from agentcourt import AgentCourt

court = AgentCourt()
ruling = court.file_dispute(
    policy="api-quality",
    claim="API returned XML",
    desired_remedy="full_refund",
    metadata={"response_received": True, "schema_matches": False}
)
print(f"Ruling: {ruling.ruling}")
```

## Why Open Source?

Agent commerce needs shared infrastructure. Just like TCP/IP is shared, dispute resolution standards should be open and community-driven. That's why AgentCourt is MIT licensed.

We want the community to:
- Contribute new policy templates
- Test the existing rules against real-world scenarios
- Build SDKs for more languages
- Integrate with agent frameworks

## What's Next?

- **Reputation system** — rulings create case law and trust scores
- **API + SDK for marketplace integration** — platforms enforce rulings
- **Evidence ingestion** — content hashing, provenance, chain of custody
- **Appeal system** — human fallback for edge cases

---

**Links:**
- [GitHub](https://github.com/vbkotecha/agentcourt-api)
- [Live API Docs](https://agentcourt-api-production.up.railway.app/docs)
- [Quick Start](https://github.com/vbkotecha/agentcourt-api/blob/main/QUICKSTART.md)
- [Integration Guide](https://github.com/vbkotecha/agentcourt-api/blob/main/docs/INTEGRATION_GUIDE.md)

If you're building agent commerce infrastructure, I'd love to hear how you handle disputes. Drop a comment below! 👇
