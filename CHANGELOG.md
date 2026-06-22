# Changelog

All notable changes to AgentCourt are documented in this file.

## [1.0.0] — 2026-06-22

### Added
- **4 policy templates** (21 rules total):
  - `freelance-delivery` (6 rules): non-delivery, late delivery, on-time, partial, disputed acceptance, rejected quality
  - `milestone-payment` (5 rules): completed-unpaid, completed-paid, incomplete, partially-complete, disputed-completion
  - `bug-bounty` (5 rules): valid-full-payout, non-reproducible, partial-severity, disclosure-violation, disputed-reproducibility
  - `sla-monitoring` (5 rules): uptime-violation, latency-breach, partial-degradation, incidents-within-sla, insufficient-monitoring
- **Policy engine** with evidence scoring, fact extraction, and deterministic rule evaluation
- **REST API** with 5 endpoints: health, policies, disputes, verdicts, cases
- **Interactive Swagger UI** at `/swagger`
- **OpenAPI 3.0.3 spec** at `/openapi.yaml`
- **API documentation** at `/api-docs`
- **Interactive demos** at `/demos` for all 4 policy templates
- **Verdict dashboard** at `/verdicts` with 21 public rulings
- **Python SDK** (`agentcourt` on PyPI)
- **JavaScript/TypeScript SDK** (`@agentcourt/sdk` on npm)
- **MCP server** for Claude/AI agent integration
- **Postman collection** for one-click API testing
- **Integration guide** with 3 patterns (marketplace escrow, SLA monitoring, bug bounty)
- **Comprehensive test suite** — 17/17 tests passing across all policy templates
- **Landing page** with live ruling engine preview

### Engine Features
- Evidence scoring with type-based weights (0.0–1.0)
- Fact extraction from natural language evidence
- Content hash verification bonus (+0.1 confidence)
- Recency scoring (30-day window)
- Reliability multipliers (high/medium/low)
- Negative phrase detection for delivery, payment, and reproducibility
- Disputed acceptance handling (null vs true/false)
- Independent assessment preference for severity scoring
- SLA latency extraction that skips contract evidence
- Partial delivery detection with proportional remedies

### Infrastructure
- Deployed on Railway (auto-deploy from git)
- CORS enabled for all origins
- Stateless architecture (no database required for v1)
- Average ruling time: <500ms

## [1.1.0] — 2026-06-22

### Added — Protocol Compatibility
- **ADRP adapter** (`src/engine/adrp_adapter.py`) — IETF draft-stone-adrp-00 compatibility
  - Maps AgentCourt remedies → ADRP verdicts (release/refund/partial)
  - Maps 21 policy rules → ADRP semantic claim codes
  - Produces ADRP RulingBundle artifacts from AgentCourt rulings
  - Implements `verify_ruling_bundle()` per ADRP Section 16.1
  - Generates `EscrowDirective` for AP2/x402/VCAP payment rails
  - Canonical JSON (JCS-compatible) for deterministic hashing
  - Optional Ed25519 signing support
  - 11/11 adapter tests passing
- **BCP integration example** (`examples/bcp_integration.py`)
  - Converts BCP DISPUTE state → AgentCourt dispute
  - Extracts evidence from BCP session messages
  - Generates BCP-compatible settlement directive
  - Demonstrates full chain: BCP → AgentCourt → Settlement → ADRP

### Added — Documentation
- **ROADMAP.md** — 6 milestones, partnership targets, design partner program, non-goals
- **FAQ.md** — 15 questions covering general, technical, integration, and security
- **ADRP_COMPATIBILITY.md** — deep analysis of IETF draft-stone-adrp-00 alignment
- **DEPLOY_FIX.md** — step-by-step Railway deploy fix guide
- **STATUS_REPORT_JUN22.md** — overnight session summary for morning review

### Added — Content
- **8 blog posts/articles** covering market positioning, technical architecture, and ADRP implementation
- **X/Twitter launch thread** (9 tweets) for @AgentCourtHQ
- **Interactive demo script** (`scripts/demo.sh`) — 4 real scenarios, colorized output
- **Investor pitch deck outline** (10 slides, confidential)

### Added — Research
- Competitive analysis of 4 competitors (Tribunal, BCP Protocol, ADRP, Arbitova)
- June 2026 agent commerce landscape mapped
- IETF draft-stone-adrp-00 full spec analyzed
- Tribunal (kalashshah/tribunal) deep dive — LLM-based judge, 0G Chain, Gensyn AXL
- BCP Protocol (lucidedev/bcp-protocol) deep dive — DISPUTE state has no resolver

### Added — Community Files
- **CONTRIBUTING.md** — contribution guide and policy template authoring
- **CODE_OF_CONDUCT.md** — Contributor Covenant 2.1
- **Dockerfile** — container build specification
- **LICENSE** — MIT

### Changed
- Updated README competitive comparison table (4 competitors)
- Added ADRP positioning note to README

### Infrastructure
- Total commits: 55
- Total files: 73
- Total tests: 28/28 passing (17 engine + 11 ADRP adapter)
- Dependencies: standard library only (Python SDK + engine)
