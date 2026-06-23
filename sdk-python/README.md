# AgentCourt Python SDK

Policy-driven dispute resolution for AI agent commerce.

## Install

```bash
pip install agentcourt
```

## Quick Start

```python
from agentcourt import AgentCourt

court = AgentCourt()

# File a dispute
ruling = court.file_dispute(
    policy="api-quality",
    claim="API returned XML instead of JSON",
    desired_remedy="full_refund",
    metadata={"response_received": True, "schema_matches": False},
)

print(f"Ruling: {ruling.ruling}")        # full_refund
print(f"Confidence: {ruling.confidence}")  # 0.90
print(f"Case ID: {ruling.case_id}")
```

## Available Policies

| Policy | Use Case |
|--------|----------|
| `api-quality` | Schema mismatch, wrong format |
| `freelance-delivery` | Non-delivery, late delivery |
| `milestone-payment` | Unpaid milestones |
| `bug-bounty` | Severity disputes |
| `sla-monitoring` | Uptime violations |
| `scope-dispute` | Budget exceedance |
| `physical-commerce` | Damaged goods |

## Links

- [API Docs](https://agentcourt-api-production.up.railway.app/docs)
- [GitHub](https://github.com/vbkotecha/agentcourt-api)
