# AgentCourt vs Arbitova: Choosing a Dispute Resolution Layer

Both AgentCourt and Arbitova solve the same problem: what happens when agent commerce transactions go wrong. They take fundamentally different approaches.

## TL;DR

| | AgentCourt | Arbitova |
|---|---|---|
| **Approach** | Policy-driven (rules engine) | LLM-based (N=3 majority vote) |
| **Speed** | <500ms | ~30s |
| **Determinism** | Same input = same ruling | Non-deterministic |
| **Cost** | $0.05 flat per dispute | 2% of transaction value |
| **Escrow** | Not required | Required (smart contract) |
| **Appeals** | Built-in appeal + human fallback | escalate_to_human flag |
| **Transparency** | Full rule-based reasoning | LLM reasoning (opaque) |
| **Blockchain** | x402 payments, verdict attestation | Full on-chain escrow lifecycle |
| **License** | MIT | Proprietary |

## When to Choose AgentCourt

- You need **fast, predictable rulings** (API quality checks, SLA monitoring)
- You want **low cost** dispute resolution ($0.05 vs 2%)
- You **don't want escrow** (direct payments, reputation-based enforcement)
- You need **auditable, deterministic** outcomes
- You have **structured evidence** (booleans, numbers, dates)

## When to Choose Arbitova

- You need **full escrow lifecycle** (lock funds, deliver, confirm)
- Disputes are **nuanced/qualitative** (content quality, creative work)
- You want **on-chain enforcement** (smart contract custody)
- You're building a **marketplace** with buyer/seller protection

## When to Use Both

AgentCourt and Arbitova are complementary:

1. **AgentCourt** handles clear-cut violations (schema mismatch, non-delivery, SLA breach)
2. **Arbitova** handles nuanced disputes where judgment is needed
3. Escalation chain: policy check → LLM arbitration → human review

```
Dispute filed
  → AgentCourt: policy-driven ruling (<500ms, $0.05)
  → If confidence < 0.70 or ambiguous: escalate to Arbitova (LLM, 30s, 2%)
  → If still unclear: human review
```

## Architecture Comparison

### AgentCourt (Non-Custodial)

```
Agent A pays Agent B via x402 (direct, no escrow)
  → Transaction goes wrong
  → AgentCourt evaluates structured evidence
  → Returns deterministic ruling
  → Marketplace adjusts reputation / triggers refund
```

### Arbitova (Escrow-Based)

```
Agent A locks USDC in Arbitova smart contract
  → Agent B delivers work
  → Agent A confirms or disputes
  → If disputed: Arbitova arbiter evaluates (LLM, 30s)
  → Smart contract releases/refunds based on verdict
```

## Policy Templates

AgentCourt ships with 7 specialized policy templates:

1. **api-quality** (7 rules): Schema mismatch, wrong format, stale data
2. **freelance-delivery** (5 rules): Non-delivery, late delivery, partial
3. **milestone-payment** (6 rules): Unpaid milestones, partial payments
4. **bug-bounty** (5 rules): Reproducibility, severity disputes
5. **sla-monitoring** (6 rules): Uptime, latency, availability
6. **scope-dispute** (4 rules): Budget exceedance, unauthorized changes
7. **physical-commerce** (6 rules): Damaged goods, wrong items, returns

Arbitova uses a single general-purpose arbitration model.

## Links

- AgentCourt: [GitHub](https://github.com/vbkotecha/agentcourt-api) | [API](https://agentcourt-api-production.up.railway.app/docs)
- Arbitova: [GitHub](https://github.com/jiayuanliang0716-max/Arbitova) | [Website](https://arbitova.com)


## AgentCourt vs aubinhaba/dispute-resolution-agent

| Dimension | AgentCourt | dispute-resolution-agent |
|-----------|-----------|------------------------|
| Approach | Deterministic rules (no LLM for ruling) | Multi-agent LLM (Spring AI) |
| Language | Python (FastAPI) | Java (Spring Boot) |
| Determinism | Guaranteed — same input → same output | Probabilistic — validation layer attempts to enforce consistency |
| Speed | <500ms | Multiple seconds (LLM inference) |
| Cost | $0.05/dispute | LLM API cost per dispute |
| Focus | Agent commerce (x402, API quality, SLA) | Payment chargebacks (traditional finance) |
| Rules | JSON policy templates, community-contributable | RAG over rule corpus |
| Audit trail | Matched rule ID + confidence | citedRulePassages + evidenceRefs |
| MCP | Native MCP server (6 tools) | MCP client for transaction data |
| API | REST + SDK + Postman | Not exposed as API |
| License | MIT | Unknown |

**Key insight:** This competitor validates the market need for dispute resolution in automated transactions. Their approach (LLM + validation) is the opposite of ours (deterministic rules). Both agree on the importance of auditability, but we achieve it through simpler means — if the rule is deterministic, the audit is automatic.

**AgentCourt advantage:** No LLM means no hallucination risk in rulings, no per-dispute inference cost, and consistent reproducibility for trust scoring.


## Market Ecosystem (June 2026)

AgentCourt doesn't exist in isolation. Here's how we fit into the emerging agent commerce stack:

| Layer | Project | What They Do | Relationship |
|-------|---------|--------------|--------------|
| **Identity** | [Open Agent Trust Registry](https://github.com/FransDevelopment/open-agent-trust-registry) | Root-of-trust for agent identity (Ed25519 attestations) | **Complementary** — Their identity + our disputes = complete trust |
| **Governance** | [Microsoft Agent Governance Toolkit](https://github.com/microsoft/agent-governance-toolkit) | Policy enforcement, zero-trust for AI agents (4.4K★) | **Adjacent** — Governance before transaction, disputes after |
| **Payments** | x402 Protocol | HTTP 402 → USDC micropayments | **Integration** — We use x402 for per-dispute pricing |
| **Audio Licensing** | [Resonate](https://github.com/akoita/resonate) | Machine-first audio licensing for agentic commerce | **Potential customer** — License disputes could use our API |
| **LLM Disputes** | [AI Dispute Resolution](https://github.com/Hardikdhawan2904/ai-dispute-resolution-system) | Enterprise dispute resolution with AI | **Differentiator** — LLM-based vs our deterministic approach |

### The Trust Stack

```
┌─────────────────────────────────────────┐
│  Governance (MS Toolkit, etc.)          │ ← Pre-transaction rules
├─────────────────────────────────────────┤
│  Identity (Trust Registry, A2A)         │ ← Who are you?
├─────────────────────────────────────────┤
│  Discovery (Directories, Marketplaces)  │ ← How do I find you?
├─────────────────────────────────────────┤
│  Payment (x402, USDC)                   │ ← How do I pay you?
├─────────────────────────────────────────┤
│  ★ DISPUTE (AgentCourt) ★              │ ← What happens when it goes wrong?
├─────────────────────────────────────────┤
│  Reputation (Phase 2)                   │ ← What's your track record?
└─────────────────────────────────────────┘
```

We're the layer nobody else is building — and the one the stack needs most.
