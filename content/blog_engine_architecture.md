# How AgentCourt's Policy Engine Works: A Technical Deep Dive

*June 2026*

When we set out to build a dispute resolution engine for agent commerce, we had one constraint that shaped every design decision: **determinism**.

The same evidence must always produce the same ruling. Not usually. Not with 95% confidence. Always.

This post explains how we achieved that.

---

## The Pipeline

```
Dispute Request
    ↓
1. Evidence Scoring → weighted facts
    ↓
2. Fact Extraction → NLP-derived claims
    ↓
3. Rule Evaluation → policy rules vs facts
    ↓
4. Ruling Generation → matched rule + remedy + confidence
```

Each stage is deterministic. No LLM in the critical path. No probabilistic reasoning. Pure logic.

---

## Stage 1: Evidence Scoring

Every piece of evidence has a type. Each type carries a default weight:

```python
EVIDENCE_WEIGHTS = {
    "contract":      1.00,
    "payment_proof": 0.90,
    "payment":       0.80,
    "invoice":       0.80,
    "receipt":       0.80,
    "commit":        0.85,
    "log":           0.80,
    "file":          0.70,
    "message":       0.70,
    "screenshot":    0.50,
    "testimonial":   0.30,
    "claim":         0.10,
}
```

A signed contract carries more weight than a screenshot. A git commit carries more weight than a chat message. This is common sense encoded as data.

### Modifiers

Three modifiers adjust the base weight:

- **Content hash present**: +0.10 (verifiable evidence is more trustworthy)
- **Recency**: evidence from the last 30 days gets a bonus, scaled linearly
- **Reliability**: explicit `high`/`medium`/`low` multiplier from the submitter

### Final Score

```
final_weight = base_weight × reliability_multiplier + (0.10 if content_hash else 0) + recency_bonus
```

Capped at 1.0.

---

## Stage 2: Fact Extraction

This is where NLP meets determinism. We use pattern-based extraction — not LLMs — to pull structured facts from natural language evidence.

### Example

Evidence: *"Seller delivered 3 of 5 required mockups on June 19"*

The extractor identifies:

```json
{
  "evidence_of_delivery": true,
  "delivery_count": 3,
  "expected_count": 5,
  "delivery_date": "2026-06-19",
  "partial_delivery_detected": true
}
```

### Negative Phrase Detection

This was the hardest engineering problem. Consider:

- ✅ *"Design files were exported and delivered to the client"*
- ❌ *"No design files were exported or delivered"*

Both contain "design files", "exported", "delivered". A naive extractor would mark both as evidence of delivery.

Our solution: a curated library of negative phrase patterns that flip the extraction result:

```python
NEGATIVE_DELIVERY_PHRASES = [
    "no design files exported",
    "nothing was delivered",
    "no deliverables received",
    "delivery not completed",
    "no evidence of delivery",
    "files were never sent",
    ...
]
```

When a negative phrase is detected, `evidence_of_delivery` is set to `false` regardless of keyword matches.

The same pattern applies to payment detection, reproducibility claims, and SLA measurements.

---

## Stage 3: Rule Evaluation

Each policy template defines rules as boolean expressions over the extracted facts:

```json
{
  "id": "non-delivery",
  "condition": "evidence_of_delivery == false AND (contract_exists OR deadline_passed)",
  "confidence": "medium",
  "remedy": "full_refund"
}
```

The evaluator:

1. Collects all extracted facts into a namespace
2. Evaluates each rule's condition against the namespace
3. Returns the first matching rule (rules are ordered by specificity)

### Disputed Facts

When evidence from both parties conflicts, we don't discard it — we track it as a disputed fact:

```json
{
  "fact": "evidence_of_delivery",
  "claimant_says": "true",
  "respondent_says": "false",
  "evidence_weight": {"claimant": 0.7, "respondent": 0.8},
  "resolved_value": "false",
  "reason": "respondent evidence carries higher weight"
}
```

The fact is resolved in favor of the higher-weighted evidence, but the dispute is transparent in the ruling output.

---

## Stage 4: Ruling Generation

The matched rule produces a ruling object:

```json
{
  "case_id": "be4d2dc6-e51a-4f3c-b2e7-...",
  "status": "resolved",
  "matched_rule_id": "non-delivery",
  "confidence": "medium",
  "ruling": "The respondent failed to deliver...",
  "reasoning": "Evidence establishes non-delivery: contract obligates delivery by June 20, no delivery evidence found...",
  "remedy": "full_refund",
  "facts_established": [...],
  "facts_disputed": [...],
  "facts_unknown": [...]
}
```

### Confidence Bands

- **High**: Multiple high-weight evidence sources agree, no contradictions
- **Medium**: Sufficient evidence to match a rule, but some gaps or disputes
- **Low**: Minimal evidence, rule matched on defaults — consider escalation

---

## Why Not Use an LLM?

We considered using GPT-4 or Claude for dispute evaluation. We chose not to, for three reasons:

1. **Determinism**: An LLM might rule differently on identical evidence depending on temperature, context window, or prompt phrasing. In dispute resolution, that's unacceptable.

2. **Auditability**: Our engine can explain exactly why a ruling was made — which evidence contributed which weight, which facts were extracted, which rule matched. An LLM's explanation is post-hoc rationalization.

3. **Cost and latency**: Our engine runs in <500ms for $0 per ruling. An LLM call costs money and adds latency.

LLMs are excellent for fact extraction (Stage 2), and we may add LLM-assisted extraction as an option. But the rule evaluation (Stage 3) must be deterministic.

---

## Test Coverage

17 test cases across 4 policy templates:

| Policy | Tests | Scenarios |
|--------|-------|-----------|
| freelance-delivery | 5 | Non-delivery, late delivery, partial, disputed acceptance, rejected quality |
| milestone-payment | 4 | Completed-unpaid, completed-paid, incomplete, partially-complete |
| bug-bounty | 4 | Valid full payout, non-reproducible, partial severity, disclosure violation |
| sla-monitoring | 4 | Uptime violation, latency breach, partial degradation, within SLA |

Every test uses realistic evidence: contracts, git commits, monitoring logs, payment receipts, chat messages.

---

## Architecture Choice: Stateless

AgentCourt is stateless. Each dispute is evaluated independently. No database. No state to manage.

This was deliberate:

- **No infrastructure**: Deploy as a single container
- **Horizontal scaling**: Every request is independent
- **No data privacy concerns**: We don't store your disputes
- **Simplicity**: Less code, fewer bugs, faster iteration

The trade-off: no case history (the calling platform tracks this). We believe this is the right trade-off for v1.

---

## Try It

The entire engine is live and free to test:

- **Interactive demos**: `/demos`
- **Swagger UI**: `/swagger`
- **OpenAPI spec**: `/openapi.yaml`
- **Python SDK**: `pip install agentcourt`
- **Source code**: MIT licensed

We're looking for design partners. If you're building agent commerce infrastructure, let's talk.
