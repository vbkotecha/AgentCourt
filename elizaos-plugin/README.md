# AgentCourt ElizaOS Plugin

Dispute resolution plugin for [ElizaOS](https://github.com/elizaOS/eliza) agents.

When your agent engages in commerce (pays for APIs, hires other agents, buys services) and things go wrong, this plugin lets your agent file disputes and get deterministic rulings.

## Install

```bash
npm install @agentcourt/elizaos-plugin
```

## Configuration

Add to your agent's `.env`:
```
AGENTCOURT_BASE_URL=https://agentcourt-api-production.up.railway.app
AGENTCOURT_API_KEY=  # optional, for paid tier
```

## Actions

| Action | Description |
|--------|-------------|
| `FILE_DISPUTE` | File a dispute and get a ruling |
| `CHECK_POLICIES` | List available policy templates |

## Available Policies

- `api-quality` — Schema mismatch, wrong format
- `freelance-delivery` — Non-delivery, late delivery
- `milestone-payment` — Unpaid milestones
- `bug-bounty` — Severity disputes
- `sla-monitoring` — Uptime violations
- `scope-dispute` — Budget exceedance
- `physical-commerce` — Damaged goods

## Links

- [AgentCourt API Docs](https://agentcourt-api-production.up.railway.app/docs)
- [GitHub](https://github.com/vbkotecha/agentcourt-api)
