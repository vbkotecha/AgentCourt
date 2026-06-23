# Changelog

All notable changes to AgentCourt are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-06-23

### Added
- **scope-dispute policy template** — 5 rules for agent mandate violations
  - `mandate-exceeded-full-refund`: Unauthorized action, no prior consent
  - `mandate-exceeded-partial`: Unauthorized but prior consent exists
  - `budget-exceeded`: Spend over authorized limit with overage calculation
  - `within-mandate-no-violation`: Action was within scope
  - `ambiguous-mandate`: Undefined scope → escalate to human review
- **Dockerfile** for one-command self-hosting (`docker-compose up`)
- **AGENTS.md** for AI agent discovery and integration
- **llms.txt** for machine-readable project description
- **scope_dispute_demo.py** — 3 real-world scenarios using Python SDK
- **GitHub Discussions** — community entry point with welcome announcement
- **FUNDING.yml** — GitHub sponsor button
- **CHANGELOG.md** — this file
- **Market validation research** — 5 authoritative sources confirming product-market fit

### Changed
- Bug-bounty policy: metadata override for `bug_reproducible` / `bug_severity`
- README updated: 7 policy templates, 39 rules, scope-dispute in policy table
- GitHub repo: 20 topics for discoverability, homepage set to live API docs
- Description updated to reflect ERC-8183 alignment

### Fixed
- Bug-bounty template always returning `valid-bug-full-payout` — metadata fields were ignored (#8711fbf)

## [1.0.0] - 2026-06-22

### Added
- **Core API** — FastAPI with 6 endpoints for dispute submission and verdict retrieval
- **6 policy templates, 34 rules:**
  - `freelance-delivery` (5 rules): non-delivery, late delivery, partial delivery
  - `milestone-payment` (6 rules): unpaid milestones, overdue, partial payments
  - `bug-bounty` (5 rules): reproducibility, severity, disclosure compliance
  - `sla-monitoring` (6 rules): uptime, latency, degraded service
  - `api-quality` (6 rules): schema mismatch, wrong types, stale data, missing fields
  - `physical-commerce` (6 rules): wrong item, damage, non-delivery, returns
- **Policy Engine** — deterministic rule matching with evidence scoring and fact extraction
- **3 SDKs** (all zero-dependency):
  - Python: `agentcourt_python_sdk.py`
  - JavaScript: `agentcourt.js`
  - TypeScript: `agentcourt.d.ts`
- **x402 middleware** — $0.05/dispute pricing, OpenAPI payment annotations, `.well-known/x402` manifest
- **ADRP adapter** — Implements Layers 1-3 of IETF draft-stone-adrp-00
- **Postman collection** for API testing
- **MCP server config** for Claude Desktop, Cursor, Claude Code
- **docker-compose.yml** with healthcheck
- **GitHub community files:** CONTRIBUTING.md, issue templates (bug report, feature request, policy template), PR template
- **Test suite** — 39 tests covering policy engine, ADRP adapter, x402 middleware
- **Production deployment** on Railway with 50+ verdicts resolved

### Standards
- ERC-8183: AgentCourt fulfills the "Evaluator" role
- ADRP: Layers 1-3 of IETF draft-stone-adrp-00
- x402: USDC on Base, x402scan indexed (16 endpoints)
