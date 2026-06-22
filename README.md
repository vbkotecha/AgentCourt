# AgentCourt

**The dispute layer for agent commerce.**

Visa, Mastercard, and Google are building payment rails for AI agents (ACP, UCP, AP2, x402). Nobody is building the dispute resolution layer. That's us.

Submit evidence. Apply policy rules. Get a deterministic ruling. No escrow, no courtroom theater.

## Why AgentCourt?

The agent commerce stack has three layers:
1. **Transport** — A2A, MCP (how agents talk)
2. **Payment** — x402, AP2, Visa Intelligent Commerce (how agents pay)
3. **Dispute** — **AgentCourt** (what happens when something goes wrong)

When an agent misfires, hallucinates a product, breaches an SLA, or delivers partial work — who resolves it? The existing card network dispute process wasn't designed for agent-initiated transactions. AgentCourt is purpose-built for this.

## Live API

**Base URL:** `https://agentcourt-api-production.up.railway.app`
**Docs:** `https://agentcourt-api-production.up.railway.app/docs`

## Quick Start

```python
from agentcourt import AgentCourt

court = AgentCourt()

ruling = court.dispute(
    claimant="ClientCorp",
    respondent="DevStudio",
    contract={
        "obligations": ["Build mobile app"],
        "deadlines": ["2026-07-01T23:59:00Z"],
        "deliverables": ["iOS app", "Android app"],
    },
    claim="Developer never delivered the app",
    desired_remedy="Full refund of deposit",
    policy="freelance-delivery",
    evidence=[
        {
            "type": "contract",
            "source": "ClientCorp",
            "timestamp": "2026-06-01T10:00:00Z",
            "claimed_fact": "Signed contract, no deliverable received",
            "reliability": "high",
        }
    ],
)

print(ruling.confidence)  # high
print(ruling.remedy)      # full_refund
print(ruling.ruling)      # The respondent failed to deliver...
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/v1/disputes` | Submit a dispute, get a ruling |
| `GET` | `/v1/cases` | List all cases |
| `GET` | `/v1/cases/{id}` | Get a specific case |
| `GET` | `/v1/policies` | List policy templates |
| `GET` | `/v1/policies/{name}` | Get policy details |
| `GET` | `/health` | API health check |
| `GET` | `/docs` | Interactive API docs (Swagger) |

## Policy Templates

### freelance-delivery
Disputes over digital work delivery: non-delivery, late delivery, scope issues.

**Rules:** non-delivery, late-delivery-accepted, late-delivery-rejected, partial-delivery, default-no-match

### milestone-payment  
Disputes over milestone payments: unpaid milestones, overdue payments, partial payments.

**Rules:** milestone-completed-unpaid, milestone-completed-paid-on-time, milestone-incomplete-payment-justified, milestone-overdue-disputed, default-no-match

### bug-bounty
Disputes over bug bounty claims: reproducibility, severity, disclosure compliance.

**Rules:** valid-bug-full-payout, non-reproducible-bug, severity-below-threshold, non-compliant-disclosure, default-no-match

### sla-monitoring
Disputes over Service Level Agreement violations: uptime, latency, response time, availability.

**Rules:** uptime-violation, latency-breach, partial-degradation, incidents-within-sla, insufficient-monitoring

## How It Works

1. **Submit evidence** — contracts, commits, logs, screenshots, payment records
2. **Evidence scoring** — each item weighted by type, reliability, recency, and hash verification
3. **Fact extraction** — structured facts derived from evidence + metadata
4. **Policy matching** — facts evaluated against policy rules (deterministic)
5. **Confidence band** — high/medium/low based on evidence quality and fact completeness
6. **Ruling generated** — with remedy, full audit trail, and explainable reasoning

## Key Design Decisions

- **No escrow required** — rulings create consequences through reputation and enforcement, not custody
- **Deterministic** — same evidence + policy always produces the same ruling
- **Explainable** — every ruling shows which rule matched, which facts were established, and evidence scores
- **Policy-first** — define rules upfront, not case-by-case
- **API-first** — REST + SDK, integrate in minutes

## SDK

### Python (zero-dependency)

```bash
pip install agentcourt  # coming soon to PyPI
```

Or copy `sdk/agentcourt.py` — zero dependencies, standard library only.

### JavaScript / TypeScript

```bash
npm install @agentcourt/sdk  # coming soon to npm
```

```javascript
const { AgentCourt } = require('@agentcourt/sdk');

const court = new AgentCourt();
const ruling = await court.resolve({
  policy: 'freelance-delivery',
  claimant: 'buyer_agent',
  respondent: 'seller_agent',
  claim: 'Deliverable never received',
  desiredRemedy: 'full_refund',
  contract: { parties: ['buyer_agent', 'seller_agent'] },
  evidence: [{ type: 'contract', source: 'agreement.json', claimedFact: 'Deadline missed' }],
});
```

Or copy `sdk/npm/index.js` — zero dependencies, works in Node 18+ and browsers.

## MCP Server

AgentCourt ships with an MCP (Model Context Protocol) server. Any MCP-aware agent framework can call AgentCourt directly.

```bash
python3 mcp_server.py
```

**5 MCP Tools:**
- `resolve_dispute` — Submit a dispute, get a ruling
- `list_policies` — See available policy templates
- `get_policy` — Read rules of a specific policy
- `get_case` — Retrieve a past case by ID
- `health_check` — Verify API status

Compatible with Letta, Claude, and any MCP-compatible agent framework.

## Architecture

```
├── src/
│   ├── main.py              # FastAPI app with REST endpoints
│   ├── engine/
│   │   └── policy_engine.py # Deterministic rule evaluation engine
│   └── policies/
│       ├── freelance-delivery.json
│       ├── milestone-payment.json
│       ├── bug-bounty.json
│       └── sla-monitoring.json
├── sdk/
│   ├── agentcourt.py        # Python SDK (zero-dependency)
│   └── npm/                 # JavaScript/TypeScript SDK
│       ├── index.js
│       ├── index.d.ts
│       └── test.js
├── mcp_server.py            # MCP server (stdio transport)
├── clawmart/
│   └── SKILL.md             # ClawMart marketplace listing
└── landing/
    └── index.html           # Landing page
```

## Why AgentCourt Exists

The agentic economy is rapidly building payment rails:

- **x402** (Coinbase) — protocol for AI agents to pay each other via USDC on Base. No dispute mechanism.
- **ERC-8183** (Ethereum draft, Feb 2026) — conditional payments and escrow for agent transactions. Explicitly states: *"no dispute resolution within the core spec."*
- **AP2** (Google) — Agent Payments Protocol. Moves money, doesn't resolve disagreements.
- **ClawBank + Shodai** — First AI-to-AI Ricardian contracts on Ethereum. Milestone logic is live. No adjudication layer.

Every major protocol handles payments, escrow, and execution. None of them handle **what happens when two agents disagree**.

AgentCourt is the missing layer. Submit evidence, apply policy rules, get a binding ruling.

**Works with any commerce protocol** — x402, ERC-8183, AP2, or custom agreements. AgentCourt doesn't hold funds. It adjudicates outcomes.

## How We Differ

| | AgentCourt | Tribunal | ADRP (SwarmSync) | Arbitova |
|---|---|---|---|---|
| **Type** | API product | On-chain court | Protocol spec (IETF draft) | Escrow + arbitration |
| **Model** | Standalone judgment layer | Multi-agent trial (lawyers, clerk, judge) | Wire protocol + state machine | Escrow + bundled arbitration |
| **Determinism** | Policy rules — same evidence = same ruling | Jury of iNFT judges — subjective | Crypto (deterministic) + Semantic (arbitration) | AI arbiter — subjective |
| **Latency** | <500ms per ruling | Full trial process (minutes/hours) | Protocol-defined | Unknown |
| **Custody** | Never. Non-custodial. | Escrow via smart contract | EscrowDirective output for rails | Holds funds in escrow |
| **Infrastructure** | Stateless API, zero deps | P2P (Gensyn AXL), 0G Chain, iNFTs | Protocol — bring your own infra | Their escrow contract |
| **Integration** | REST + SDK + MCP. Works with any platform | Deploy their court contracts | Implement the protocol | Use their escrow contract |
| **Lock-in** | None. Bring your own escrow, marketplace, payment rail | Must deploy on 0G Chain | Protocol-defined | Must use their escrow contract |

AgentCourt is not an escrow company. We don't compete with payment protocols. We are the judgment layer that any of them can call.

**Note on ADRP (IETF draft-stone-adrp-00):** ADRP defines a wire protocol for agent dispute resolution. AgentCourt's engine could serve as a backend implementation of ADRP's Semantic-class dispute resolution — we produce the `RulingBundle` that ADRP's state machine requires. This is complementary, not competitive.

## Pricing

**Design Partner Program (Now):** Free for first 5 partners. Full API access. Custom policy template included.

**Production (Post-Launch):** Per-dispute pricing. No transaction fees. No custody fees. No platform fees. You only pay when you need a ruling.

## License

MIT
