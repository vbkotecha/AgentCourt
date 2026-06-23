# AgentCourt Integration Examples

Ready-to-use code for adding dispute resolution to your AI agents.

## Examples

| Language | Framework | File |
|----------|-----------|------|
| Python | LangChain | [langchain_dispute_tool.py](./langchain_dispute_tool.py) |
| Python | CrewAI | [crewai_dispute_agent.py](./crewai_dispute_agent.py) |
| JavaScript | Node.js (fetch) | [nodejs_dispute.js](./nodejs_dispute.js) |

## Quick Start (any language)

```bash
curl -X POST https://agentcourt-api-production.up.railway.app/v1/disputes \
  -H "Content-Type: application/json" \
  -d '{
    "policy": "api-quality",
    "claim": "Schema mismatch",
    "claimant": "my-agent",
    "respondent": "api",
    "desired_remedy": "full_refund",
    "contract": {"parties": ["my-agent", "api"], "obligations": ["Return JSON"]},
    "metadata": {"response_received": true, "schema_matches": false},
    "evidence": [{"type": "log", "source": "monitor", "claimed_fact": "XML returned"}]
  }'
```

## Available Policies

| Policy | Use Case | Rules |
|--------|----------|-------|
| `api-quality` | API schema/response disputes | 7 |
| `freelance-delivery` | Work delivery disputes | 5 |
| `milestone-payment` | Milestone payment disputes | 6 |
| `bug-bounty` | Bounty severity disputes | 5 |
| `sla-monitoring` | Uptime/latency disputes | 6 |
| `scope-dispute` | Scope/budget disputes | 4 |
| `physical-commerce` | Product/shipping disputes | 6 |

## Pricing

- **Free tier**: 100 disputes/month
- **Paid**: $0.05/dispute in USDC on Base (x402-native)
- **No API key required** for free tier

## Links

- [API Docs](https://agentcourt-api-production.up.railway.app/docs)
- [GitHub](https://github.com/vbkotecha/agentcourt-api)
- [Full Integration Guide](https://github.com/vbkotecha/agentcourt-api/discussions/3)
