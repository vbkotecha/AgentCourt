# AgentCash × AgentCourt Partnership Proposal

## The Opportunity

AgentCash indexes 3,200+ paid APIs. Every paid call is a potential dispute:

- API returns wrong data → user paid $0.028 for garbage
- API schema doesn't match documentation → user paid for unexpected response
- API is down but still charges → user paid for nothing
- API quality degrades after payment → user paid for inferior service

Today, when an AgentCash user gets a bad API response, they lose their USDC. There is no refund mechanism. No dispute process. No resolution path.

**AgentCourt fixes this.**

## Proposed Integration

### MCP Tool Addition

Add an `agentcourt_dispute` tool to the AgentCash MCP server:

```
Tool: agentcourt_dispute
Input: {
  endpoint: "https://api.example.com/data",
  amount_paid: "0.028 USDC",
  tx_hash: "0x...",
  expected_schema: {...},
  actual_response: {...},
  claim: "Response data does not match schema",
  policy: "api-quality"
}
Output: {
  ruling: "full_refund" | "partial_refund" | "no_match",
  confidence: "high" | "medium" | "low",
  reasoning: "...",
  matched_rule: "schema-mismatch"
}
```

### Refund Flow

When AgentCourt rules `full_refund`, AgentCash:
1. Verifies the ruling (hash-chained, deterministic)
2. Credits the user's wallet with the disputed amount
3. Debits the API provider's balance (or flags for manual review in v1)

### New Policy Template

AgentCourt will build a custom `api-quality` policy template for AgentCash with rules covering:

| Rule | Trigger | Remedy |
|------|---------|--------|
| schema-mismatch | Response doesn't match OpenAPI schema | full_refund |
| empty-response | 200 OK but empty/null body | full_refund |
| wrong-data-type | Field types don't match declared types | full_refund |
| partial-response | Required fields missing | partial_refund |
| service-unavailable | 402 charged but service returned error | full_refund |
| stale-data | Data timestamp older than declared freshness | partial_refund |

### Automatic Quality Scoring

Every dispute ruling feeds into an API quality score. APIs with high dispute rates get flagged in the AgentCash directory. This creates a trust signal for agents choosing which APIs to call.

## Why AgentCourt (Not an LLM Judge)

AgentCash handles real money. USDC payments. When you're refunding money, you need:

1. **Determinism** — Same evidence = same ruling. An LLM might refund one user and deny another for the same bad API response. AgentCourt's policy rules are deterministic.
2. **Speed** — Sub-500ms ruling. LLM-based systems take minutes.
3. **Auditability** — Every ruling cites the exact rule matched and evidence scores. Fully explainable.
4. **Cost** — No LLM tokens per dispute. Standard library computation only.

## What We Bring

- 4 policy templates, 21 rules, 28/28 tests
- ADRP-compatible (IETF draft-stone-adrp-00)
- MCP server already built
- Non-custodial (we never touch funds, just produce rulings)
- MIT licensed (self-host for free)

## What We Need From AgentCash

1. **Technical integration call** — 30 minutes to map AgentCash's dispute patterns to policy rules
2. **API access** — Ability to create a custom `api-quality` policy template
3. **Co-marketing** — Joint announcement: "AgentCash now has dispute resolution"

## Timeline

- **Week 1:** Build `api-quality` policy template (6 rules)
- **Week 2:** Test with AgentCash team, refine rules
- **Week 3:** Ship `agentcourt_dispute` tool in AgentCash MCP server
- **Week 4:** Public announcement, blog post, case study

## Contact

- **Email:** hello@agentcourt.ai
- **MoltX:** @AgentCourt
- **GitHub:** github.com/vbkotecha/agentcourt-api

---

*AgentCourt — The dispute layer for agent commerce. Deterministic. API-first. Now with API quality disputes.*
