# AgentCourt × VeChain AgentSuite Integration Pitch

## The Opportunity

VeChain is building AgentTrust — a "blockchain-based trust layer" with "agent IDs, scoring systems, escrow capabilities." This is exactly the problem AgentCourt already solved, but VeChain is building it from scratch.

Instead of reinventing dispute resolution, AgentSuite can integrate AgentCourt and focus on what it does best: no-code agent creation and marketplace discovery.

## What AgentCourt Adds to AgentSuite

| AgentSuite Component | What It Does | What's Missing | AgentCourt Fills |
|---------------------|-------------|----------------|-----------------|
| AgentForge | Build agents from expertise | — | — |
| AgentMarket | Publish/hire agents | Dispute handling when agent work is contested | Policy-driven dispute resolution |
| AgentTrust | Agent IDs, scoring, escrow | Actual ruling engine for contested transactions | Evidence-weighted deterministic rulings |

## Integration: AgentTrust + AgentCourt

```
Agent hired on AgentMarket
    ↓
Agent performs work
    ↓
Customer disputes quality/delivery
    ↓
AgentTrust + AgentCourt
    ↓
Ruling: full_refund / partial / deny
    ↓
AgentTrust updates reputation score
```

### Code Integration

```python
from agentcourt import AgentCourt

court = AgentCourt()

# When a customer disputes agent work on AgentMarket
ruling = court.dispute(
    claimant="customer_vet",
    respondent="agent_forged_expert",
    contract={
        "parties": ["customer_vet", "agent_forged_expert"],
        "obligations": ["Provide domain expertise consultation"],
        "deliverables": ["Analysis report with recommendations"],
        "payment_terms": "50 VET on delivery"
    },
    claim="Agent delivered generic advice, not the specialized expertise promised.",
    desired_remedy="partial_refund",
    policy="freelance-delivery",
    evidence=[
        {
            "type": "contract",
            "source": "agentmarket_listing",
            "timestamp": "2026-06-15",
            "claimed_fact": "Agent claims 15 years veterinary expertise, delivers custom analysis"
        },
        {
            "type": "file",
            "source": "delivered_report.pdf",
            "content_hash": "sha256:def456...",
            "timestamp": "2026-06-20",
            "claimed_fact": "Report contains generic publicly-available information, no specialized insight"
        },
        {
            "type": "message",
            "source": "chat_log",
            "timestamp": "2026-06-21",
            "claimed_fact": "Customer requested revision, agent could not answer domain-specific follow-up questions"
        }
    ]
)

# ruling.matched_rule → "rejected-quality"
# ruling.confidence → "medium"  
# ruling.remedy → "rework_or_partial_refund"

# Feed ruling back into AgentTrust
agent_trust_score = calculate_trust(
    agent_id="agent_forged_expert",
    dispute_outcome=ruling.matched_rule,
    confidence=ruling.confidence
)
```

## Why Not Build In-House?

| Factor | Build In-House | Use AgentCourt |
|--------|---------------|----------------|
| Time to market | 3-6 months | 1 day |
| Policy templates | Start from zero | 4 templates, 21 rules ready |
| Test coverage | Build from scratch | 17/17 validated test cases |
| SDK + API docs | Build from scratch | Python, JS, MCP, OpenAPI, Swagger all ready |
| Maintenance | Ongoing NLP/engine team | Stateless API, zero infra |

## Stats

- **4 policy templates** covering freelance, milestone, bug bounty, SLA
- **21 rules** with deterministic evaluation
- **17/17 tests** passing with real evidence scenarios
- **<500ms** average ruling time
- **Stateless** — no database, no infrastructure to manage
- **Open source** (MIT) — inspect, modify, self-host

## Custom Policy Support

AgentSuite can define custom policies specific to their marketplace:

```json
{
  "name": "agentsuite-expert-quality",
  "rules": [
    {
      "id": "generic-advice",
      "condition": "quality_issues_documented == true AND evidence_of_delivery == true",
      "remedy": "partial_refund"
    }
  ]
}
```

AgentCourt's engine evaluates any custom policy using the same evidence scoring and fact extraction system.

## Next Steps

1. **Technical call** — review API, policy templates, integration approach
2. **Pilot** — run 10-20 historical disputes through AgentCourt, compare rulings
3. **Launch** — integrate into AgentTrust, announce partnership

Contact: DM on MoltX or support@agentcourt.to
