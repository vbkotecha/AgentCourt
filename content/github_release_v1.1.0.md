# Release v1.1.0 — ADRP Compatible, 6 Policy Templates, BCP Integration

## 🎉 What's New

### Protocol Compatibility
- **ADRP Adapter** — AgentCourt is now the first product-level implementation of an ADRP-compatible resolution engine for [IETF draft-stone-adrp-00](https://datatracker.ietf.org/doc/html/draft-stone-adrp-00)
  - Produces signed RulingBundles from AgentCourt rulings
  - Implements `verify_resolution()` per ADRP Section 16.1
  - Generates EscrowDirectives for AP2/x402/VCAP payment rails
  - Maps all semantic claim codes to policy templates
  - 11/11 adapter tests passing

### New Policy Templates
- **`api-quality`** (7 rules) — Disputes for paid API calls: schema mismatch, empty response, wrong data types, partial response, service unavailable, stale data. Designed for [AgentCash](https://agentcash.dev) integration (3,200+ x402 APIs).
- **`physical-commerce`** (6 rules) — Disputes for agent-purchased physical products: non-delivery, wrong product, damaged in transit, not as described, return denied. Designed for [Rye](https://rye.com) x402 checkout integration.

### Integration Examples
- **BCP Protocol integration** — Full end-to-end demo resolving a [BCP](https://github.com/lucidedev/bcp-protocol) DISPUTE session through AgentCourt, producing both a settlement directive and an ADRP RulingBundle.

### Documentation
- **ROADMAP.md** — 6 milestones, partnership targets, design partner program, non-goals
- **FAQ.md** — 15 questions covering general, technical, integration, security
- **ADRP_COMPATIBILITY.md** — Deep analysis of IETF draft alignment
- **CHANGELOG.md** — Full v1.0 and v1.1 changelog

### Content
- 10 blog posts covering market positioning, ADRP implementation, and June 2026 market analysis
- Interactive demo script (`scripts/demo.sh`) — 4 real scenarios with colorized output
- Design partner one-pager and investor pitch deck outline

## 📊 Numbers

| Metric | v1.0.0 | v1.1.0 |
|--------|--------|--------|
| Policy templates | 4 | **6** (+2) |
| Total rules | 21 | **34** (+13) |
| Tests | 17/17 | **28/28** (+11) |
| SDKs | 3 | 3 |
| Integration examples | 0 | **2** |
| Documentation files | 10 | **16** |

## 🔧 Technical Details

### Dependencies
- Python SDK + engine: standard library only (zero dependencies)
- ADRP adapter: standard library (Ed25519 signing optional via `cryptography`)
- JavaScript SDK: zero dependencies, Node 18+ and browser compatible

### API
- Latency: <500ms per dispute
- Architecture: stateless, horizontally scalable
- License: MIT

### Protocol Support
- ADRP (IETF draft-stone-adrp-00) — RulingBundle production, verify_resolution, EscrowDirective
- BCP Protocol — DISPUTE state resolution
- MCP — Native Model Context Protocol server
- Non-custodial — AgentCourt never holds funds

## 🚀 Design Partner Program

Seeking 5 design partners. Free API access (100 disputes/day), custom policy template, and direct roadmap input. Target verticals:

1. Agent marketplaces (ClawMart)
2. Payment platforms (AgentCash, x402)
3. Bug bounty platforms (BotBounty)
4. SaaS/API providers (SLA disputes)
5. Physical commerce (Rye)

Contact: hello@agentcourt.ai or DM on MoltX

## 📝 Full Changelog

See [CHANGELOG.md](CHANGELOG.md) for detailed changes.

---

**Install:**
```bash
pip install agentcourt        # Python
npm install @agentcourt/sdk   # JavaScript
```

**Quick Start:**
```python
from agentcourt import AgentCourt

court = AgentCourt()
ruling = court.resolve(
    policy="api-quality",
    claimant="my_agent",
    respondent="weather_api",
    claim="API returned wrong data type",
    evidence=[...],
)
print(ruling.remedy)  # full_refund
```
