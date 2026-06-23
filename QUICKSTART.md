# AgentCourt Quick Start

**Time to first ruling: 2 minutes. Zero installation required.**

---

## Option 1: cURL (30 seconds)

```bash
curl -X POST https://agentcourt-api-production.up.railway.app/v1/disputes \
  -H "Content-Type: application/json" \
  -d '{
    "claimant": "my-agent",
    "respondent": "bad-api",
    "contract": {"parties": ["my-agent", "bad-api"], "obligations": ["Return JSON"]},
    "claim": "API returned XML instead of JSON",
    "desired_remedy": "full_refund",
    "evidence": [{"type": "log", "source": "monitor", "timestamp": "2026-01-01T00:00:00Z", "claimed_fact": "Content-Type was text/xml"}],
    "policy": "api-quality",
    "metadata": {"response_received": true, "schema_matches": false}
  }'
```

## Option 2: Python (1 minute)

```bash
# No install needed — uses stdlib only
python3 -c "
import urllib.request, json

data = json.dumps({
    'claimant': 'my-agent',
    'respondent': 'bad-api',
    'contract': {'parties': ['my-agent','bad-api'], 'obligations': ['Return JSON']},
    'claim': 'API returned XML',
    'desired_remedy': 'full_refund',
    'evidence': [{'type':'log','source':'monitor','timestamp':'2026-01-01T00:00:00Z','claimed_fact':'XML returned'}],
    'policy': 'api-quality',
    'metadata': {'response_received': True, 'schema_matches': False}
}).encode()

req = urllib.request.Request(
    'https://agentcourt-api-production.up.railway.app/v1/disputes',
    data=data, headers={'Content-Type': 'application/json'}, method='POST'
)
print(json.loads(urllib.request.urlopen(req).read()))
"
```

## Option 3: Python SDK (2 minutes)

```bash
# Clone and use the SDK
git clone https://github.com/vbkotecha/agentcourt-api.git
cd agentcourt-api/sdk-python
pip install -e .
```

```python
from agentcourt import AgentCourt

court = AgentCourt()

# Check health
print(court.health())
# {'status': 'ok', 'policies': ['api-quality', 'freelance-delivery', ...]}

# List policies
policies = court.list_policies()
for p in policies:
    print(f"  {p.name}: {p.description}")

# File a dispute
ruling = court.file_dispute(
    policy="api-quality",
    claim="API returned XML instead of JSON",
    desired_remedy="full_refund",
    metadata={"response_received": True, "schema_matches": False},
)
print(f"Ruling: {ruling.ruling}")
print(f"Confidence: {ruling.confidence}")
print(f"Case ID: {ruling.case_id}")
```

## Option 4: JavaScript (2 minutes)

```bash
git clone https://github.com/vbkotecha/agentcourt-api.git
cd agentcourt-api/sdk-js
npm install
```

```javascript
import { AgentCourt } from "@agentcourt/sdk";

const court = new AgentCourt();

const ruling = await court.fileDispute({
  policy: "api-quality",
  claim: "API returned XML instead of JSON",
  desiredRemedy: "full_refund",
  metadata: { response_received: true, schema_matches: false },
});

console.log(ruling.ruling);     // "full_refund"
console.log(ruling.confidence); // "0.90"
```

## Option 5: MCP Server (for Claude/Cursor)

Add to your MCP config:

```json
{
  "mcpServers": {
    "agentcourt": {
      "command": "python3",
      "args": ["path/to/mcp-server/server.py"]
    }
  }
}
```

Then ask Claude: "File a dispute — the API returned XML instead of JSON."

## Available Policies

| Policy | Use Case | Key Metadata Fields |
|--------|----------|-------------------|
| `api-quality` | Schema mismatch, wrong format | `response_received`, `schema_matches` |
| `freelance-delivery` | Non-delivery, late delivery | `delivered`, `meets_spec`, `response_received` |
| `milestone-payment` | Unpaid milestones | `milestone_completed`, `completion_percentage`, `milestone_paid` |
| `bug-bounty` | Severity disputes | `bug_reproducible`, `severity_claimed`, `severity_actual` |
| `sla-monitoring` | Uptime violations | `uptime_percentage`, `sla_threshold`, `downtime_minutes` |
| `scope-dispute` | Budget exceedance | `budget_exceeded`, `scope_changed`, `original_scope` |
| `physical-commerce` | Damaged goods | `damaged`, `as_described`, `return_requested` |

## Pricing

- **Free tier**: 100 disputes/month, no auth required
- **Paid**: $0.05/dispute in USDC on Base (x402 protocol)

## Links

- [Full API Docs](https://agentcourt-api-production.up.railway.app/docs)
- [GitHub](https://github.com/vbkotecha/agentcourt-api)
- [Architecture](https://github.com/vbkotecha/agentcourt-api/blob/main/docs/architecture.md)
- [API Examples](https://github.com/vbkotecha/agentcourt-api/blob/main/docs/API_EXAMPLES.md)
- [Comparison vs Arbitova](https://github.com/vbkotecha/agentcourt-api/blob/main/docs/comparison.md)
