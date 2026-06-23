# AgentCourt

> The Evaluator layer for agent commerce.

Policy-driven dispute resolution API. Submit evidence → apply rules → get a deterministic ruling in under 500ms.

## For AI Agents

### Live API
- Base URL: `https://agentcourt-api-production.up.railway.app`
- OpenAPI Docs: `/docs`
- Health: `/health`
- Policies: `GET /v1/policies`
- Create Dispute: `POST /v1/disputes`
- Verdicts: `GET /v1/verdicts`

### Quick Start
```
POST /v1/disputes
Content-Type: application/json

{
  "policy": "api-quality",
  "claim": "API returned wrong data type",
  "claimant": "buyer_agent",
  "respondent": "weather_api",
  "desired_remedy": "full_refund",
  "contract": {"parties": ["buyer_agent", "weather_api"], "obligations": ["Match OpenAPI schema"]},
  "metadata": {"response_received": true, "schema_matches": false},
  "evidence": [{"type": "log", "source": "response.json", "timestamp": "2026-06-22", "claimed_fact": "Wrong data type returned"}]
}
```

### Response Format
```json
{
  "dispute_id": "case_xxx",
  "policy": "api-quality",
  "matched_rule_id": "schema-mismatch",
  "ruling": "Schema mismatch confirmed...",
  "remedy": "full_refund",
  "confidence": "high",
  "processing_time_ms": 14
}
```

### Available Policies

| Policy | Use Case | Key Facts Required |
|--------|----------|-------------------|
| `freelance-delivery` | Non-delivery, late delivery, partial delivery | `deliverable_was_accepted`, `delivery_was_on_time`, `evidence_of_delivery` |
| `milestone-payment` | Unpaid milestones, overdue payments | `milestone_completed`, `payment_received`, `days_since_completion`, `payment_terms_days` |
| `bug-bounty` | Reproducibility, severity, disclosure | `bug_is_reproducible`, `severity_meets_threshold`, `disclosure_compliant`, `reproduction_attempts` |
| `sla-monitoring` | Uptime, latency, degraded service | `actual_uptime`, `required_uptime`, `actual_latency`, `max_latency`, `monitoring_period_confirmed` |
| `api-quality` | Schema mismatch, wrong types, stale data | `response_received`, `schema_matches`, `response_is_empty`, `data_type_correct` |
| `physical-commerce` | Wrong item, damage, non-delivery | `delivery_confirmed`, `received_matches_order`, `shipping_damage`, `days_since_order`, `delivery_window_days` |

### Worked Examples (Copy-Paste Ready)

#### 1. Freelance Non-Delivery
```json
{
  "policy": "freelance-delivery",
  "claim": "Developer delivered nothing after deadline",
  "claimant": "startup_client",
  "respondent": "freelance_dev",
  "desired_remedy": "full_refund",
  "contract": {"parties": ["startup_client", "freelance_dev"], "obligations": ["Build MVP by June 1"]},
  "metadata": {"deliverable_was_accepted": false, "evidence_of_delivery": false},
  "evidence": [{"type": "log", "source": "github", "timestamp": "2026-06-15T00:00:00Z", "claimed_fact": "No commits after May 20"}]
}
```
→ Matched rule: `non-delivery` | Remedy: `full_refund`

#### 2. SLA Uptime Violation
```json
{
  "policy": "sla-monitoring",
  "claim": "API uptime at 95.2% vs 99.9% SLA guarantee",
  "claimant": "consumer_app",
  "respondent": "data_provider",
  "desired_remedy": "service_credit",
  "contract": {"parties": ["consumer_app", "data_provider"], "obligations": ["99.9% uptime SLA"]},
  "metadata": {"actual_uptime": 95.2, "required_uptime": 99.9, "monitoring_period_confirmed": true},
  "evidence": [{"type": "metric", "source": "datadog", "timestamp": "2026-06-22T00:00:00Z", "claimed_fact": "Monthly uptime 95.2%"}]
}
```
→ Matched rule: `uptime-violation` | Remedy: `service_credit`

#### 3. Bug Bounty — Valid Critical
```json
{
  "policy": "bug-bounty",
  "claim": "SQL injection in /api/login endpoint",
  "claimant": "security_researcher",
  "respondent": "fintech_startup",
  "desired_remedy": "full_payout",
  "contract": {"parties": ["security_researcher", "fintech_startup"], "obligations": ["Bug bounty program"]},
  "metadata": {"bug_is_reproducible": true, "severity_meets_threshold": true, "disclosure_compliant": true},
  "evidence": [{"type": "report", "source": "pentest", "timestamp": "2026-06-20T00:00:00Z", "claimed_fact": "SQLi confirmed with PoC"}]
}
```
→ Matched rule: `valid-bug-full-payout` | Remedy: `full_payout`

#### 4. Physical Commerce — Wrong Item
```json
{
  "policy": "physical-commerce",
  "claim": "Ordered red sneakers, received blue sandals",
  "claimant": "shopper_agent",
  "respondent": "marketplace_seller",
  "desired_remedy": "replacement",
  "contract": {"parties": ["shopper_agent", "marketplace_seller"], "obligations": ["Deliver red sneakers size 10"]},
  "metadata": {"delivery_confirmed": true, "received_matches_order": false},
  "evidence": [{"type": "photo", "source": "delivery_photo.jpg", "timestamp": "2026-06-22T00:00:00Z", "claimed_fact": "Blue sandals received, not red sneakers"}]
}
```
→ Matched rule: `wrong-product` | Remedy: `replacement`

### Integration via SDK

**Python:**
```python
from agentcourt import AgentCourt

court = AgentCourt(api_url="https://agentcourt-api-production.up.railway.app")
verdict = court.create_dispute(
    policy="api-quality",
    claim="Wrong data type returned",
    claimant="my_agent",
    respondent="data_api",
    desired_remedy="full_refund",
    contract={"parties": ["my_agent", "data_api"], "obligations": ["Return string type"]},
    metadata={"response_received": True, "schema_matches": False},
    evidence=[{"type": "log", "source": "response", "timestamp": "2026-06-22", "claimed_fact": "Got int instead of string"}]
)
print(verdict["matched_rule_id"])  # → "schema-mismatch"
```

**JavaScript / TypeScript:**
```javascript
import { AgentCourt } from './sdk/agentcourt.js';

const court = new AgentCourt('https://agentcourt-api-production.up.railway.app');
const verdict = await court.createDispute({
  policy: 'api-quality',
  claim: 'Wrong data type returned',
  claimant: 'my_agent',
  respondent: 'data_api',
  desiredRemedy: 'full_refund',
  contract: { parties: ['my_agent', 'data_api'], obligations: ['Return string type'] },
  metadata: { response_received: true, schema_matches: false },
  evidence: [{ type: 'log', source: 'response', timestamp: '2026-06-22', claimed_fact: 'Got int instead of string' }]
});
console.log(verdict.matched_rule_id); // → "schema-mismatch"
```

### MCP Server (Claude Desktop / Cursor / Claude Code)
```json
{
  "mcpServers": {
    "agentcourt": {
      "command": "python3",
      "args": ["-m", "agentcourt.mcp"],
      "env": {
        "AGENTCOURT_URL": "https://agentcourt-api-production.up.railway.app"
      }
    }
  }
}
```

### Pricing
$0.05/dispute via x402 (USDC on Base). Free tier: 100 disputes/month.

### Self-Hosting
```bash
git clone https://github.com/vbkotecha/agentcourt-api.git
cd agentcourt-api
docker-compose up -d
# API available at http://localhost:8000
```

### Architecture
- **Policy-first**: Define dispute rules upfront, not ad-hoc LLM judgments
- **Evidence-native**: Content hashing, provenance, chain of custody
- **Multi-mode**: Auto-checks → rubric → AI mediation → arbitration → human
- **API-first**: REST + SDKs + webhooks
- **Auditability**: Every ruling has a traceable rule match + evidence chain
- **Non-custodial**: Pure evaluation layer, no escrow, no financial regulation

### Links
- GitHub: https://github.com/vbkotecha/agentcourt-api
- Live API: https://agentcourt-api-production.up.railway.app
- License: MIT
- E2E Tests: `python3 tests/test_e2e_all_policies.py`
