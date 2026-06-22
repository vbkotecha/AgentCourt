# AgentCourt vs The Field — Technical Comparison

## Quick Answer

AgentCourt is the only **deterministic, API-first, non-custodial** dispute resolution engine built for agent commerce. Every alternative either uses non-deterministic LLM judgment, requires escrow lock-in, or is just a protocol spec with no implementation.

## Comparison Matrix

| Feature | AgentCourt | Tribunal | BCP Protocol | Arbitova | Kleros |
|---------|-----------|----------|-------------|----------|--------|
| **Determinism** | ✅ Same evidence = same ruling | ❌ LLM-based | N/A | Unknown | ❌ Human jury |
| **API-first** | ✅ REST + SDKs | ❌ Smart contract | ✅ DISPUTE state | ✅ | ❌ DApp |
| **Escrow required** | ❌ Never | Depends on chain | ✅ Mandatory | ✅ Mandatory | ✅ Mandatory |
| **Non-custodial** | ✅ | ❌ On-chain escrow | ❌ | ❌ | ❌ |
| **Protocol standard** | ADRP (IETF) | None | BCP | None | None |
| **MCP native** | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Self-host** | ✅ MIT | ❌ Heavy infra | N/A | ❌ | ❌ |
| **Dependencies** | Zero | 0G Chain, Gensyn | Ethereum | Unknown | Ethereum |
| **Latency** | <500ms | Minutes (chain) | Block time | Unknown | Hours/days |
| **Cost/dispute** | $0.01-0.10 | Gas fees | Gas fees | Unknown | Juror fees |
| **LLM in critical path** | ❌ Never | ✅ Judge agent | N/A | Unknown | ❌ |
| **Audit trail** | ✅ Full reasoning | LLM output | On-chain | Unknown | Vote records |

---

## Deep Dives

### AgentCourt
**What:** Policy-driven dispute resolution API. Submit evidence → apply rules → get ruling.
**How:** Deterministic Python rule engine. 6 policy templates, 34 rules. Evidence scoring with type-based weights. No database required.
**Best for:** Any platform that needs automated dispute resolution at scale.
**Limitation:** Requires policy templates to be authored in advance. Cannot handle novel dispute types without a new template.

### Tribunal (github.com/kalashshah/tribunal)
**What:** Multi-agent on-chain court system with LLM-based judge agents.
**How:** Agents present cases on 0G Chain. Gensyn AXL handles compute. LLM judges evaluate and produce verdicts. ENS for identity.
**Best for:** High-stakes crypto disputes where on-chain verifiability matters more than speed or determinism.
**Limitation:** Non-deterministic by design. Same case could get different rulings from different judge runs. Heavy infrastructure. Gas costs per dispute. "The Supreme Court model" — powerful but slow and expensive.

### BCP Protocol (github.com/lucidedev/bcp-protocol)
**What:** Protocol standard for agent session management with a DISPUTE state.
**How:** Agents transact in sessions. Either party can invoke DISPUTE, which freezes escrow. But BCP has no resolution engine — it just freezes funds and waits.
**Best for:** Standardizing agent session lifecycle and escrow management.
**Limitation:** Has the DISPUTE state but no resolver. AgentCourt fills this gap — we built the integration example (`examples/bcp_integration.py`).

### Arbitova
**What:** Agent arbitration platform requiring their escrow service.
**How:** Agents deposit funds into Arbitova escrow. Disputes are resolved through their (proprietary) system.
**Best for:** Platforms that want end-to-end escrow + arbitration from a single provider.
**Limitation:** Custodial lock-in. You must use their escrow. Closed system. No self-hosting.

### Kleros
**What:** Decentralized court protocol using human juror panels.
**How:** Disputes go to randomly selected human jurors who vote on outcomes. PNK token staking for juror selection.
**Best for:** Subjective disputes requiring human judgment (e.g., content moderation, subjective quality).
**Limitation:** Hours to days for resolution. Juror fees. Non-deterministic. Built for human-scale dispute volume, not agent-scale (millions/day).

---

## The Determinism Argument

In dispute resolution, **non-determinism is a bug, not a feature.**

If two agents submit identical evidence for identical disputes and get different rulings, the system is unfair. This is why:

- **Tribunal's LLM judge** cannot guarantee consistency
- **Kleros's human jurors** inherently produce varied outcomes
- **AgentCourt's policy rules** produce identical rulings for identical evidence, every time

Determinism enables:
1. **Auditability** — Regulators can verify fairness
2. **Predictability** — Platforms know what to expect
3. **Trust** — No "the judge was in a bad mood" risk
4. **Scale** — No human/LLM bottleneck

## When to Use Each

| Use Case | Recommended |
|----------|-------------|
| API quality disputes | AgentCourt (`api-quality` template) |
| Physical commerce disputes | AgentCourt (`physical-commerce` template) |
| Freelance delivery disputes | AgentCourt (`freelance-delivery` template) |
| SLA monitoring disputes | AgentCourt (`sla-monitoring` template) |
| Milestone payment disputes | AgentCourt (`milestone-payment` template) |
| Bug bounty disputes | AgentCourt (`bug-bounty` template) |
| Session/escrow management | BCP Protocol (+ AgentCourt for resolution) |
| High-stakes crypto arbitration | Tribunal |
| Subjective content disputes | Kleros |

---

*Last updated: June 22, 2026. This comparison is based on publicly available information and our analysis. We welcome corrections from the teams listed above.*
