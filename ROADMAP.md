# AgentCourt Roadmap

## Vision

Every agent commerce transaction will eventually need dispute resolution. AgentCourt aims to be the default resolution layer — the Stripe Radar of agent commerce. Deterministic, instant, API-first.

## Current State (June 2026)

**Live and working:**
- ✅ Policy engine with 4 templates, 21 rules, 17/17 tests
- ✅ REST API (11 endpoints) with Swagger docs
- ✅ Python SDK (zero-dependency)
- ✅ JavaScript/TypeScript SDK
- ✅ MCP server for agent frameworks
- ✅ ADRP adapter (draft-stone-adrp-00 compatible)
- ✅ BCP integration example
- ✅ Interactive demo script (4 scenarios)

---

## Milestones

### M1: Core Engine ✅ Complete
- Deterministic policy rule evaluation
- Evidence scoring and fact extraction
- 4 policy templates (freelance, milestone, bug bounty, SLA)
- Confidence bands (high/medium/low)
- Full audit trail in ruling output

### M2: Protocol Compatibility ✅ Complete
- ADRP RulingBundle adapter (IETF draft-stone-adrp-00)
- verify_resolution implementation
- EscrowDirective output for payment rails
- BCP Protocol integration example
- 11/11 ADRP adapter tests

### M3: Developer Experience ← You are here
**In progress:**
- [ ] GitHub public repo (code ready, needs push)
- [ ] npm package (@agentcourt/sdk)
- [ ] PyPI package (agentcourt)
- [ ] Hosted API (Railway — needs deploy fix)
- [ ] Interactive playground (web UI for trying disputes)

**Next:**
- [ ] TypeScript native SDK (currently JS with .d.ts)
- [ ] Go SDK
- [ ] Rust SDK
- [ ] CLI tool (`agentcourt resolve --policy freelance-delivery --evidence ...`)

### M4: Policy Ecosystem
- [ ] Policy template registry (community-contributed)
- [ ] Policy validation tool (lint your templates before use)
- [ ] Custom policy SDK (define rules in Python/YAML)
- [ ] Policy marketplace (browse and adopt templates)
- [ ] Policy versioning and migration

Templates planned:
- [ ] NFT marketplace disputes (mint quality, royalty disputes)
- [ ] DeFi liquidation disputes (oracle manipulation claims)
- [ ] API access disputes (rate limit, data quality)
- [ ] Data licensing disputes (usage rights, attribution)
- [ ] AI model output disputes (hallucination claims, quality)

### M5: Trust & Precedent
- [ ] Precedent corpus (index rulings by template hash — ADRP Layer 5)
- [ ] Reputation scores (based on ruling history)
- [ ] Ed25519 signed rulings with AgentCourt DID
- [ ] Verifiable Credentials for AgentCourt as arbitrator
- [ ] IANA "ADRP Trusted Arbitrator Registries" application
- [ ] Ruling citation system (arbitrators cite or distinguish prior rulings)

### M6: Scale & Operations
- [ ] Stateless horizontal scaling (already stateless, needs infra)
- [ ] Rate limiting and API keys
- [ ] Usage analytics dashboard
- [ ] Webhook notifications for ruling completion
- [ ] Batch dispute submission API
- [ ] Sub-100ms latency optimization

---

## Integration Partnerships

### Target Platforms (in priority order)

| Platform | Why | Status |
|----------|-----|--------|
| **BCP Protocol** | Has DISPUTE state but no resolution engine | Integration example built |
| **x402 (Coinbase)** | Payment protocol, needs dispute layer | Researching |
| **AP2 (Google)** | Agent Payments Protocol | Researching |
| **ClawMart** | Agent marketplace | Listed on marketplace |
| **MoltX** | Agent social network | 16 accounts engaged |
| **0G / Tribunal** | On-chain court (complementary, not competitive) | Analyzed |

### ADRP Ecosystem
AgentCourt is positioned as the first product-level implementation of an ADRP-compatible resolution engine. As the ADRP spec matures through IETF, AgentCourt will:
1. Track spec updates and maintain compliance
2. Participate in interop testing
3. Serve as reference implementation for Semantic-class disputes
4. Apply for Trusted Arbitrator Registry status

---

## Design Partner Program

**Goal:** 5 design partners in Q3 2026

**What partners get:**
- Free API access (up to 100 disputes/day)
- One custom policy template built for their use case
- Direct input on roadmap priorities
- Co-marketing opportunity (case study)

**Target verticals:**
1. Freelance/gig marketplaces (milestone disputes)
2. Bug bounty platforms (severity/reproducibility disputes)
3. SaaS/API providers (SLA disputes)
4. Agent marketplaces (quality/scope disputes)
5. DeFi protocols (oracle/liquidation disputes)

---

## Non-Goals (What We Don't Build)

- **Escrow** — AgentCourt never holds funds. Platforms enforce rulings.
- **Identity** — AgentCourt doesn't verify who you are. Bring your own identity.
- **LLM-based judgment** — Determinism is a feature. No LLM in the critical path.
- **Courtroom simulation** — No lawyers, no trials, no multi-agent deliberation.
- **On-chain enforcement** — AgentCourt produces rulings. Chains enforce them.
- **Token** — No token, no governance token, no stake-weighted arbitration.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to contribute.

**Highest-impact contributions right now:**
1. New policy templates (see M4 planned list)
2. SDK ports (Go, Rust)
3. Integration examples (x402, AP2, custom)
4. Test coverage for edge cases
5. Documentation translations

---

*This roadmap is a living document. Priorities shift based on design partner feedback and market developments. Last updated: June 22, 2026.*
