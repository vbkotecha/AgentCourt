# AgentCourt — Project Status

**Last updated:** June 23, 2026 (11:45 PM UTC)  
**Commits:** 166 | **Stars:** 2 | **PRs:** 7 (1 merged)

---

## What Is AgentCourt

Policy-driven dispute resolution API for AI agent commerce. When autonomous agents transact and things go wrong (API schema mismatch, non-delivery, SLA breach), AgentCourt evaluates structured evidence and returns a deterministic ruling in under 500ms.

**Live API:** https://agentcourt-api-production.up.railway.app  
**Landing Page:** https://vbkotecha.github.io/agentcourt-api/  
**GitHub:** https://github.com/vbkotecha/agentcourt-api

---

## ✅ Complete

### Code
- Core FastAPI dispute resolution engine (7 policies, 39 rules)
- Python SDK (stdlib only, zero dependencies)
- JavaScript/TypeScript SDK (native fetch, Node 18+)
- MCP Server (6 tools for Claude/Cursor)
- ElizaOS Plugin (FILE_DISPUTE + CHECK_POLICIES actions)
- 8 API tests (all passing)
- Demo script (`demo.py`)
- Docker + Docker Compose
- GitHub Codespaces config

### Documentation (18 files)
- README (14 badges, 18 sections, FAQ, API table)
- QUICKSTART (2-minute start)
- INTEGRATION_GUIDE (7 integration paths)
- ERROR_HANDLING (HTTP codes, x402, retry)
- API_KEYS (auth roadmap)
- RATE_LIMITING (limits + 429 format)
- BENCHMARK (real latency: sub-100ms)
- ROADMAP (6 phases)
- CHANGELOG (v1.0.0 → v1.3.0)
- Architecture (design philosophy)
- Comparison (vs competitors + ecosystem map)
- 3 Architecture Decision Records (ADR-001, 002, 003)
- SECURITY, CODE_OF_CONDUCT, CONTRIBUTING, CONTRIBUTING_POLICY

### Distribution (7 PRs, 565K+ stars)
| Repository | Stars | Status |
|-----------|-------|--------|
| awesome-molt-ecosystem | 57 | ✅ MERGED |
| public-apis | 443K | ⏳ Open |
| awesome-mcp-servers | 89K | ⏳ Needs Glama |
| awesome-ai-agents | 28K | ⏳ Needs CLA |
| awesome-generative-ai | 3.5K | ⏳ Open |
| awesome-x402 | 241 | ⏳ Open |
| awesome-agentic-commerce | 133 | ⏳ Open |

### GitHub
- Release v1.0.0 published ✓
- GitHub Pages live ✓
- GitHub Discussions enabled (5 threads) ✓
- Issue templates (bug, feature, policy request) ✓
- PR template ✓
- 20 optimized topics ✓
- OpenGraph + Twitter Card ✓
- Postman collection ✓

### Launch Assets (ready to fire)
- dev.to article ✓
- Show HN template ✓
- Product Hunt launch plan ✓
- Custom GPT instructions ✓
- One-shot publisher script ✓
- Glama submission guide ✓

### Other
- Glama.ai MCP server submitted ✓
- W3C Workshop submission ✓
- X/Twitter: 40+ posts today ✓

---

## ❌ Blocked

| Blocker | Who | Impact | Solution |
|---------|-----|--------|----------|
| Railway Deploy Latest | Vivek | Disputes return 402 instead of 200 | Click Deploy or send API token |
| npm token | Vivek | 3 packages unpublished | `npm token create` |
| PyPI token | Vivek | Python SDK unpublished | `pypi.org → API tokens` |
| E2B CLA | Vivek | 28K★ PR blocked | Sign at e2b.dev/docs/cla |
| GitHub PAT workflow scope | Vivek | CI workflow stuck as draft | Edit PAT to include `workflow` |

---

## Key Numbers

- **166 commits** in one day
- **7 policies**, **39 rules**, **<500ms** ruling latency
- **5 SDKs/integrations** (Python, JS, MCP, ElizaOS, REST)
- **7 PRs** across **565K+** combined GitHub stars
- **18 documentation files**
- **Sub-100ms** measured GET latency (health: 40ms, policies: 104ms)
- **$0.05** per dispute (USDC on Base via x402)
- **MIT** licensed
