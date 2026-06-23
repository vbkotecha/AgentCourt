# AgentCourt JavaScript SDK

Policy-driven dispute resolution for AI agent commerce.

## Install

```bash
npm install @agentcourt/sdk
```

## Quick Start

```javascript
import { AgentCourt } from "@agentcourt/sdk";

const court = new AgentCourt();

// File a dispute
const ruling = await court.fileDispute({
  policy: "api-quality",
  claim: "API returned XML instead of JSON",
  desiredRemedy: "full_refund",
  metadata: { response_received: true, schema_matches: false },
});

console.log(ruling.ruling);     // "full_refund"
console.log(ruling.confidence); // 0.90
console.log(ruling.case_id);
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
