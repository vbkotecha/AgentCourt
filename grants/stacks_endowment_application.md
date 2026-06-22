# Stacks Endowment Q2 Builder Grant Application — AgentCourt

## Getting Started Grant ($10,000)

### Project: AgentCourt — Policy-Driven Dispute Resolution for Agent Commerce

---

## 1. PROJECT OVERVIEW

AgentCourt is an autonomous dispute resolution API that serves as the trust layer for AI agent commerce. As agents increasingly transact on Bitcoin L2s and beyond, they need a way to resolve disputes when transactions fail — without human intervention, without custodial escrow, and without slow legal processes.

AgentCourt provides instant, policy-driven rulings via a single REST API endpoint. It's live, deployed, and processing real disputes today.

**Live API:** https://agentcourt-api-production.up.railway.app  
**Dashboard:** https://agentcourt-api-production.up.railway.app/verdicts  
**Docs:** https://agentcourt-api-production.up.railway.app/docs

---

## 2. PROBLEM BEING SOLVED

The agentic economy is exploding:
- **400K+ active AI agents** transacting autonomously
- **$43M+ in agent-to-agent transactions** processed in 2026
- **165M transactions** via x402 alone
- **Mastercard AP4M** launched June 2026 with 30+ partners

Yet NONE of these payment protocols include dispute resolution:
- **x402** (Coinbase): No dispute mechanism
- **ERC-8183**: Explicitly excludes disputes from spec
- **Mastercard AP4M**: No recourse for failed agent transactions
- **x402r**: Arbiter-agnostic but no reference implementation

When an agent pays for a service that isn't delivered, when a milestone is completed but payment never comes, when a bug bounty is downgraded to avoid payout — there is no resolution mechanism. AgentCourt fills this gap.

---

## 3. WHY STACKS / BITCOIN L2 ECOSYSTEM

AgentCourt is chain-agnostic but naturally aligned with Bitcoin L2s:

1. **Base integration already live** — x402 payments settle on Base (Bitcoin L2 via Coinbase)
2. **sBTC compatibility** — AgentCourt can resolve disputes involving sBTC transactions between agents
3. **Stacks smart contracts** — Policy engine output can trigger Clarity contract execution for automated remedy enforcement
4. **Trustless by design** — Non-custodial, deterministic rulings don't require trusting a central authority
5. **Growing agent economy on Stacks** — As DeFi agents proliferate on Stacks, dispute resolution becomes essential infrastructure

The Bitcoin L2 ecosystem needs trust infrastructure for autonomous agents. AgentCourt provides it.

---

## 4. TECHNICAL ARCHITECTURE

### Policy Engine (Core Innovation)
Unlike competitors using subjective AI arbitration, AgentCourt uses **deterministic policy rules**:

- **4 policy templates, 21 rules total:**
  - freelance-delivery (6 rules): non-delivery, late delivery, scope, partial delivery
  - milestone-payment (5 rules): unpaid milestones, overdue payments, partial payments
  - bug-bounty (5 rules): reproducibility, severity, disclosure compliance
  - sla-monitoring (5 rules): uptime, latency, degradation, incident response

### How It Works
```
Agent submits: contract + evidence + claim
  → Policy engine matches dispute to rule set
  → Extracts facts from evidence (NLP + structured parsing)
  → Scores evidence reliability (0.0-1.0)
  → Evaluates rules against established facts
  → Returns: ruling + confidence + reasoning + remedy + audit trail
```

### Evidence Scoring
Each piece of evidence gets a reliability score based on type, source, and claimed fact. Conflicting evidence is weighted. Low-evidence cases escalate rather than guessing.

### Audit Trail
Every ruling includes:
- Matched rule ID + policy template
- Facts established, disputed, and unknown
- Per-evidence scores with reasoning
- Confidence band (high/medium/low)
- Full timestamp chain

### Integrations
- **x402 payment middleware** ($0.50/ruling via USDC on Base)
- **Python SDK** (zero-dependency)
- **npm SDK** (`@agentcourt/sdk`, TypeScript types)
- **MCP Server** (5 tools, JSON-RPC, for AI agent integration)

---

## 5. TEAM

**Vivek Kotecha — Founder**
- Software engineer based in San Francisco
- Currently at OpusClip (AI video platform)
- Previously at Hayden AI
- Building AgentCourt as AI-native infrastructure
- H1B visa secured, fully committed to this project

**HustleMode — AI Co-Founder**
- Autonomous AI agent running 24/7 on Railway
- Handles code generation, testing, deployment, distribution
- Active on MoltX agent network (posting, community engagement, partnership outreach)
- Manages cron-based operations pipeline (every 15 minutes)

---

## 6. GRANT FUND USAGE ($10,000)

| Item | Cost | Purpose |
|------|------|---------|
| Base mainnet contract deployment | $200 | Gas for AgentCourt contracts |
| ClawMart marketplace listing | $240 | $20/mo creator account (12 months) |
| Railway infrastructure | $600 | $50/mo hosting (12 months) |
| MoltX promoted content | $500 | Agent network distribution |
| OpenRouter LLM costs | $1,200 | Judge LLM inference ($100/mo, 12 months) |
| Domain + DNS | $100 | agentcourt.to renewal + CDN |
| Development bounty program | $3,000 | Pay agents to build integrations |
| Legal review of policy templates | $2,000 | Ensure ruling enforceability |
| Emergency reserve | $2,160 | Buffer for unforeseen costs |
| **TOTAL** | **$10,000** | |

---

## 7. TIMELINE AND MILESTONES

### Month 1 (July 2026)
- Deploy AgentCourt contracts on Base mainnet
- Publish SDKs to npm + PyPI
- Achieve first 10 paid rulings ($5 revenue)
- List on ClawMart marketplace
- Apply to additional grants (GOAT Network, Hedera)

### Month 2 (August 2026)
- Integrate with Stacks sBTC for Bitcoin L2 dispute resolution
- Build Clarity smart contract for automated remedy enforcement
- Onboard 3 design partner agents (from MoltX pipeline)
- Achieve 100 paid rulings ($50 revenue)

### Month 3 (September 2026)
- Launch 5th policy template (API access control)
- Publish open-source reference implementation for x402 disputes
- Achieve 500 paid rulings ($250 revenue)
- Begin token launch evaluation (if warranted by traction)

---

## 8. COMPETITIVE ADVANTAGE

| Feature | AgentCourt | Arbitova | Setix | Gavel |
|---------|-----------|----------|-------|-------|
| Policy engine (deterministic) | ✅ | ❌ | ❌ | ❌ |
| No escrow required | ✅ | ❌ | ❌ | ❌ |
| Flat fee ($0.50) | ✅ | 0.5%+2% | TBD | TBD |
| REST API | ✅ | Solidity | API | TBD |
| Live on mainnet | Soon | Testnet | Devnet | Live |
| MCP server | ✅ | ✅ | ❌ | ❌ |
| Explainable rulings | ✅ | Partial | ❌ | ✅ |

---

## 9. LINKS

- **Live API:** https://agentcourt-api-production.up.railway.app
- **Swagger Docs:** https://agentcourt-api-production.up.railway.app/docs
- **Verdict Dashboard:** https://agentcourt-api-production.up.railway.app/verdicts
- **Interactive Demos:** https://agentcourt-api-production.up.railway.app/demos
- **Domain:** agentcourt.to

---

*Submitted by Vivek Kotecha (vbkotecha@gmail.com) for the Stacks Endowment Q2 2026 Builder Grant Program.*
