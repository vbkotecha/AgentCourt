# ADR-002: No Escrow in v1

## Status
Accepted — June 2026

## Context
Should AgentCourt hold funds in escrow and release them based on rulings?

### Option A: Agent Court Holds Escrow
AgentCourt collects payment, holds it, and releases based on the ruling.

**Pros:**
- Automatic enforcement — funds move based on ruling
- Revenue stream — escrow fees

**Cons:**
- **Financial regulation** — money transmission licenses, KYC/AML compliance
- Security risk — holding funds makes us a target
- Kills velocity — regulatory compliance takes months
- Scope creep — we're a dispute resolution tool, not a payment processor

### Option B: No Escrow — Rulings Enforced Through Reputation (Chosen)
AgentCourt produces rulings. Enforcement happens through:
- Reputation scores (Phase 2)
- Marketplace policy (Phase 3)
- Precedent (Phase 2)

**Pros:**
- Ship fast — no regulatory burden
- Stateless — no fund custody, no security risk
- Platform-agnostic — any marketplace can enforce our rulings
- Focus on core competency — ruling accuracy, not fund management

**Cons:**
- Rulings are advisory, not automatically enforced
- Requires platform buy-in for enforcement
- May add optional escrow later for high-value disputes

## Decision
We chose **Option B: No Escrow in v1**.

AgentCourt v1 focuses exclusively on producing accurate, auditable rulings. Escrow is explicitly deferred to Phase 5+ when users demand it.

## Consequences
- Faster time to market (no financial regulation)
- Rulings must be enforced by platforms, not by AgentCourt directly
- Optional escrow module planned for Phase 5 for high-value disputes
- Revenue model is per-dispute pricing ($0.05), not escrow fees
