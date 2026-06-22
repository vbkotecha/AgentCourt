# GOAT Network Base Grant Application — AgentCourt

## Project: AgentCourt — Policy-Driven Dispute Resolution for Agent Commerce

### What is AgentCourt?

AgentCourt is the missing dispute resolution layer for agentic commerce. As AI agents increasingly transact autonomously — making payments, delivering services, and executing contracts — the infrastructure for resolving disputes when things go wrong doesn't exist. AgentCourt fills this gap with a policy-driven ruling API.

### The Problem

Every major agent payment protocol launched in 2026 WITHOUT dispute resolution:
- **x402** (Coinbase): 165M transactions, $50M volume, NO dispute mechanism
- **ERC-8183**: Explicitly states "no dispute resolution in core spec"
- **Mastercard AP4M**: 30+ partners, no dispute layer
- **x402r**: Arbiter-agnostic but no reference arbiter implementation

400K+ agents are spending $43M with zero recourse when transactions fail.

### Our Solution

AgentCourt provides a single REST API endpoint:

```
POST /v1/disputes → returns ruling + confidence + reasoning + remedy
```

**Key differentiators:**
1. **Policy engine** — Deterministic rule evaluation, not subjective LLM guessing
2. **4 policy templates** — freelance-delivery, milestone-payment, bug-bounty, sla-monitoring
3. **x402 integrated** — $0.50/ruling via USDC on Base
4. **No escrow required** — Works with ANY payment protocol
5. **Full audit trail** — Every ruling explainable with evidence scoring

### x402 Integration (LIVE)

AgentCourt's x402 middleware is deployed and functional:
- Each ruling costs $0.50 USDC on Base
- Payment verified before ruling is returned
- Clean integration: `x402 Payment → SignedDispute → AgentCourt API → SignedResolution`

### Economic Utility

AgentCourt enables trust in autonomous agent commerce:
- Agents can resolve disputes without human intervention
- Marketplaces can offer buyer protection without custodial risk
- Payment protocols get a reference dispute layer for free
- Revenue model: $0.50/ruling + subscription tiers for high-volume

### Grant Use ($500)

1. Deploy AgentCourt contracts on Base mainnet ($50 gas)
2. Publish SDKs to npm and PyPI ($0 — accounts ready)
3. Register on ClawMart agent marketplace ($20/mo creator account)
4. Initial marketing push on MoltX agent network ($100 promoted posts)
5. Remaining $330: API infrastructure costs (Railway hosting)

### Team

- **Vivek Kotecha** — Founder, ex-Hayden AI, San Francisco
- **HustleMode** — AI co-founder, autonomous agent running 24/7

### Links

- Live API: https://agentcourt-api-production.up.railway.app
- Docs: https://agentcourt-api-production.up.railway.app/docs
- Dashboard: https://agentcourt-api-production.up.railway.app/verdicts

