# AgentCourt Roadmap

## Current Status: v1.0.0 — Core API Live ✅

7 policy templates, 39 rules, deterministic <500ms rulings, x402-native.

---

## Phase 1: Foundation (COMPLETE ✅)

- [x] Core dispute resolution API
- [x] 7 policy templates (api-quality, freelance-delivery, milestone-payment, bug-bounty, sla-monitoring, scope-dispute, physical-commerce)
- [x] 39 deterministic rules
- [x] REST API with OpenAPI spec
- [x] Python SDK
- [x] JavaScript SDK
- [x] MCP Server (6 tools)
- [x] ElizaOS Plugin
- [x] x402 payment integration
- [x] Docker + self-hosting
- [x] Comprehensive documentation
- [x] 8 API tests
- [x] GitHub Pages landing page
- [x] GitHub Release v1.0.0

## Phase 2: Trust & Reputation (Q3 2026)

- [ ] Reputation scoring — past rulings create trust scores for agents
- [ ] Precedent system — similar disputes produce consistent rulings across cases
- [ ] Case law accumulation — rulings indexed and searchable
- [ ] Agent identity verification — link disputes to verified agent identities
- [ ] Appeal system — human fallback for edge cases

### Reputation Score Design

```
Agent Trust Score = f(
  total_disputes_filed,
  disputes_won,
  disputes_lost,
  evidence_quality_score,
  resolution_acceptance_rate,
  time_since_last_dispute
)
```

Scores update with each ruling. Platforms can query scores to decide whether to transact with an agent.

## Phase 3: Marketplace Integration (Q4 2026)

- [ ] REST + SDK for marketplace enforcement — platforms can query rulings and enforce them
- [ ] Webhook notifications — real-time ruling delivery to connected platforms
- [ ] Bulk dispute API — file multiple disputes in one request
- [ ] Custom policy builder — visual editor for creating policy templates
- [ ] Rate limiting + authentication — API keys for production use

## Phase 4: Evidence Infrastructure (Q1 2027)

- [ ] Content hashing — cryptographic proof of evidence integrity
- [ ] Provenance tracking — chain of custody for submitted evidence
- [ ] Tamper detection — verify evidence hasn't been modified
- [ ] Integration with A2A protocol — automatic evidence collection from agent communication
- [ ] Integration with x402 — automatic payment proof collection

## Phase 5: Dispute Templates Marketplace (Q2 2027)

- [ ] Community-submitted policy templates
- [ ] Template review and approval process
- [ ] Template versioning and backwards compatibility
- [ ] Specialized templates by industry (SaaS, DeFi, physical goods, creator economy)
- [ ] Template analytics — success rates, accuracy metrics

## Phase 6: Governance (Q3 2027)

- [ ] Decentralized ruling review — community validates edge-case rulings
- [ ] Policy governance — community proposes and votes on rule changes
- [ ] Transparency dashboard — all rulings public, searchable, auditable
- [ ] Optional arbitration layer — human arbitrators for high-value disputes

---

## Principles

1. **Deterministic first** — Rules, not LLMs, for the ruling path
2. **Open source** — MIT licensed, community-driven
3. **Stateless by default** — No database dependency for core rulings
4. **Privacy-preserving** — No PII stored, evidence handled by caller
5. **Platform-agnostic** — Any agent framework, any payment system, any marketplace

## How to Contribute

- [Submit a new policy template](CONTRIBUTING_POLICY.md)
- [Report a bug or request a feature](https://github.com/vbkotecha/agentcourt-api/issues)
- [Join the discussion](https://github.com/vbkotecha/agentcourt-api/discussions)
- [Star the repo](https://github.com/vbkotecha/agentcourt-api) ⭐

---

*This roadmap is a living document. Priorities may shift based on community feedback and market needs.*
