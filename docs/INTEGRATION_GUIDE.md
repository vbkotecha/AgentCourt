# AgentCourt Integration Guide

Everything you need to add dispute resolution to your agent framework or platform.

---

## Quick Decision: Which Integration?

| Your Stack | Use This | Install |
|-----------|----------|---------|
| Python | Python SDK | `pip install agentcourt` |
| Node.js/JS | JS SDK | `npm install @agentcourt/sdk` |
| Claude/Cursor | MCP Server | Add to MCP config |
| ElizaOS | ElizaOS Plugin | `npm install @agentcourt/elizaos-plugin` |
| Any (curl) | REST API | No install needed |
| CI/CD | GitHub Action | Use template in `/templates/` |

---

## 1. Python SDK

```python
from agentcourt import AgentCourt
from agentcourt.exceptions import PaymentRequiredError

court = AgentCourt()

try:
    ruling = court.file_dispute(
        policy="api-quality",
        claim="API returned XML instead of JSON",
        desired_remedy="full_refund",
        metadata={
            "response_received": True,
            "schema_matches": False
        },
        evidence=[{
            "type": "log",
            "source": "api-gateway",
            "timestamp": "2026-06-23T12:00:00Z",
            "claimed_fact": "Content-Type: text/xml"
        }]
    )
    print(f"Ruling: {ruling.ruling}")
    print(f"Confidence: {ruling.confidence}")
    print(f"Case ID: {ruling.case_id}")

except PaymentRequiredError as e:
    print(f"Free tier exceeded. Pay {e.amount} {e.asset} to {e.pay_to}")
    # Handle x402 payment here
```

## 2. LangChain Tool

```python
from langchain.tools import Tool
from agentcourt import AgentCourt

court = AgentCourt()

def file_dispute_tool(query: str) -> str:
    """File a dispute when an agent transaction fails."""
    import json
    params = json.loads(query)
    try:
        result = court.file_dispute(**params)
        return json.dumps(result.__dict__, indent=2)
    except Exception as e:
        return f"Error: {e}"

dispute_tool = Tool(
    name="file_dispute",
    description="File a dispute with AgentCourt. Pass policy, claim, desired_remedy, and metadata as JSON.",
    func=file_dispute_tool
)

# Add to your agent's tool list
agent_tools = [dispute_tool, ...]
```

## 3. CrewAI Tool

```python
from crewai.tools import BaseTool
from agentcourt import AgentCourt

court = AgentCourt()

class DisputeResolutionTool(BaseTool):
    name: str = "file_dispute"
    description: str = "File a dispute when an agent commerce transaction fails."

    def _run(self, policy: str, claim: str, metadata: dict) -> str:
        try:
            result = court.file_dispute(
                policy=policy,
                claim=claim,
                desired_remedy="full_refund",
                metadata=metadata
            )
            return f"Ruling: {result.ruling} (confidence: {result.confidence})"
        except Exception as e:
            return f"Error: {e}"

# Use in your crew
from crewai import Agent
agent = Agent(
    role="Quality Monitor",
    goal="File disputes when API transactions fail",
    backstory="...",
    tools=[DisputeResolutionTool()]
)
```

## 4. JavaScript/Node.js

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
console.log(ruling.caseId);     // "case-xxxxx"
```

## 5. MCP Server (Claude/Cursor)

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "agentcourt": {
      "command": "python3",
      "args": ["/path/to/agentcourt-api/mcp-server/server.py"]
    }
  }
}
```

Then in Claude: *"File a dispute — the API I paid for returned XML instead of JSON."*

## 6. ElizaOS Plugin

```javascript
import { AgentCourtPlugin } from "@agentcourt/elizaos-plugin";

// Register with your ElizaOS runtime
runtime.registerPlugin(AgentCourtPlugin);

// Agent can now use FILE_DISPUTE action
```

## 7. REST API (curl)

```bash
curl -X POST https://agentcourt-api-production.up.railway.app/v1/disputes \
  -H "Content-Type: application/json" \
  -d '{
    "policy": "api-quality",
    "claim": "API returned XML instead of JSON",
    "desired_remedy": "full_refund",
    "evidence": [{"type": "log", "source": "monitor", "timestamp": "2026-06-23T12:00:00Z", "claimed_fact": "XML returned"}],
    "metadata": {"response_received": true, "schema_matches": false},
    "claimant": "my-agent",
    "respondent": "bad-api",
    "contract": {"parties": ["my-agent", "bad-api"], "obligations": ["Return JSON"]}
  }'
```

---

## Choosing the Right Policy

| Scenario | Policy | Key Metadata |
|----------|--------|-------------|
| API returned wrong format | `api-quality` | `response_received`, `schema_matches` |
| Freelancer didn't deliver | `freelance-delivery` | `delivered`, `meets_spec`, `response_received` |
| Milestone payment overdue | `milestone-payment` | `milestone_completed`, `completion_percentage`, `milestone_paid` |
| Bug bounty severity dispute | `bug-bounty` | `bug_reproducible`, `severity_claimed`, `severity_actual` |
| SLA uptime breach | `sla-monitoring` | `uptime_percentage`, `sla_threshold` |
| Budget/scope exceeded | `scope-dispute` | `budget_exceeded`, `scope_changed` |
| Physical goods damaged | `physical-commerce` | `damaged`, `as_described`, `return_requested` |

---

## Handling the x402 Payment

When free tier (100/month) is exceeded, the API returns HTTP 402 with payment details:

```json
{
  "error": "PaymentRequiredError",
  "amount": "50000",
  "asset": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
  "chain": "eip155:8453",
  "pay_to": "0x9863aB6242663FCc84c33632741711dB78f8Fd15"
}
```

Use [x402 client libraries](https://github.com/x402-foundation/x402) to facilitate the USDC payment on Base, then retry the request with the payment receipt.

---

## Links

- [Quick Start](https://github.com/vbkotecha/agentcourt-api/blob/main/QUICKSTART.md)
- [API Examples](https://github.com/vbkotecha/agentcourt-api/blob/main/docs/API_EXAMPLES.md)
- [Architecture](https://github.com/vbkotecha/agentcourt-api/blob/main/docs/architecture.md)
- [API Docs](https://agentcourt-api-production.up.railway.app/docs)
