# ADR-003: Stateless Architecture

## Status
Accepted — June 2026

## Context
Should AgentCourt store dispute data between requests?

### Decision
**Stateless.** Each dispute request is evaluated independently. No database, no session state, no persistence layer.

## Rationale
- **Simplicity** — fewer moving parts, fewer failure modes
- **Scalability** — any instance can handle any request, horizontal scaling trivial
- **Privacy** — no PII stored, no data breaches possible
- **Performance** — no database lookups in the hot path
- **Cost** — no database hosting, no backup infrastructure

## Consequences
- Callers must store their own ruling responses if they need them later
- The `/v1/cases` endpoint stores only in-memory (resets on deploy)
- Phase 2 will add optional persistence for reputation scoring and precedent
- This is acceptable for v1 where most disputes are fire-and-forget
