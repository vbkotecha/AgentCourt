# ADR-001: Deterministic Rules Over LLM for Dispute Resolution

## Status
Accepted — June 2026

## Context
When designing AgentCourt, the fundamental architectural decision was: **how should dispute rulings be produced?**

Two approaches were considered:

### Option A: LLM-Based Ruling
Feed evidence + context to an LLM (GPT-4, Claude) and ask it to produce a ruling.

**Pros:**
- Flexible — can handle any dispute type
- Natural language input — no structured metadata needed
- Quick to prototype

**Cons:**
- **Non-deterministic** — same input → different output across runs
- Slow — 5-30 seconds per ruling
- Expensive — LLM API cost per dispute
- Hallucination risk — model may invent facts or rules
- Opacity — difficult to audit "why" the LLM ruled a certain way
- Version fragility — model updates can change rulings

### Option B: Deterministic Rules (Chosen)
Define policy templates as JSON with explicit conditions, rulings, and confidence scores.

**Pros:**
- **Deterministic** — same input → same output, every time
- Fast — <500ms per ruling
- Cheap — no LLM API cost
- Zero hallucination — rules evaluate booleans, numbers, dates
- Fully auditable — matched rule ID + reasoning always included
- Version stable — rules don't change unless we update them

**Cons:**
- Less flexible — requires structured metadata
- Requires upfront policy design
- Can't handle ambiguous/subjective disputes

## Decision
We chose **Option B: Deterministic Rules**.

AgentCourt's core ruling engine evaluates structured metadata against JSON policy templates. No LLM is used in the ruling path.

## Consequences
- Disputes must include structured `metadata` fields (booleans, numbers, timestamps)
- Policy templates must be designed upfront by domain experts
- We may add an LLM-based **appeal layer** in Phase 2 for edge cases
- Trust scoring and precedent become possible because rulings are reproducible

## References
- [Comparison vs aubinhaba/dispute-resolution-agent](../comparison.md) (LLM-based approach)
- [Policy Template Guide](../../CONTRIBUTING_POLICY.md)
