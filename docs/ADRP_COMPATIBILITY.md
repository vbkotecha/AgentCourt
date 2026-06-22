# AgentCourt × ADRP (draft-stone-adrp-00) Compatibility Analysis

## Executive Summary

ADRP (Agent Dispute Resolution Protocol) is an IETF draft defining the wire protocol for agent dispute resolution. AgentCourt is a production engine that produces deterministic dispute rulings. **They are complementary: ADRP defines the protocol, AgentCourt implements the engine.**

Specifically, AgentCourt maps directly to ADRP's "Resolution Engine" (Layer 3) and can produce the `RulingBundle` artifacts that ADRP's `verify_resolution` function consumes.

---

## ADRP Architecture (5 Layers)

```
Layer 5: Precedent corpus (signed RulingBundles indexed by template hash)
Layer 4: Tier router (L1 atomic / L2 mandated / L3 fiduciary)
Layer 3: Resolution engine (crypto-class auto, semantic-class arbitration) ← AGENTCOURT
Layer 2: Counter-attestation primitive (append-only override)
Layer 1: Arbitration Mandate (4th AP2 mandate, FAA Section 2)
```

## Where AgentCourt Fits

**AgentCourt = ADRP Layer 3 Resolution Engine**

ADRP bifurcates disputes into two classes:
1. **Cryptographic-class**: Resolved by code (hash verification, signature checks)
2. **Semantic-class**: Resolved by arbitration against acceptance criteria

AgentCourt handles **both classes**:
- Cryptographic: Evidence hashing, content verification, timestamp validation
- Semantic: Policy rule evaluation, evidence weighting, fact extraction

### Mapping: ADRP Semantic Claim Codes → AgentCourt Policy Templates

| ADRP Claim Code | AgentCourt Policy | AgentCourt Rules |
|---|---|---|
| `quality_mismatch` | freelance-delivery | partial-delivery, rejected-quality |
| `spec_ambiguity` | freelance-delivery | disputed-acceptance |
| `timing_breach` | sla-monitoring | uptime-violation, latency-breach |
| `fitness_for_purpose` | freelance-delivery | rejected-quality |

### Mapping: ADRP Verdicts → AgentCourt Remedies

| ADRP Verdict | AgentCourt Remedy |
|---|---|
| `release` | full_payout, delivery_accepted |
| `refund` | full_refund |
| `partial` | partial_refund (with split ratio) |

## How AgentCourt Produces an ADRP-Compatible RulingBundle

```
ADRP DisputeFiling
    ↓
AgentCourt.dispute(policy=<mapped_template>, evidence=<from DisputeBundle>)
    ↓
AgentCourt produces: {
    matched_rule_id,
    confidence: high|medium|low,
    remedy: full_refund|partial_refund|full_payout,
    reasoning: <explanation>,
    facts_established: [...],
    evidence_scores: {...}
}
    ↓
ADRP Adapter converts to:
    RulingBundle {
        verdict: map(remedy),
        partial_split: extract_split(remedy),
        rationale_hash: sha256(reasoning),
        arbitrator_did: "did:web:agentcourt.ai",
        ...
    }
```

## What AgentCourt Would Need to Add for Full ADRP Compliance

1. **Ed25519 signing** — Sign RulingBundles with an AgentCourt DID
2. **Hash chain** — Anchor rulings to DisputeBundles via SHA-256 chain
3. **Verifiable Credentials** — AgentCourt arbitrator credential from TRUSTED_REGISTRIES
4. **EscrowDirective output** — Format ruling output as ADRP's EscrowDirective
5. **DID identity** — Register `did:web:agentcourt.ai` or equivalent

**Estimated effort: 2-3 days of development.**

## Strategic Implication

ADRP validates AgentCourt's thesis at the highest level (IETF standards track). The protocol explicitly states:

> *"A valid cryptographic proof bundle equals contractual satisfaction. It does not."*

This is AgentCourt's core argument: evidence of action ≠ satisfaction of contract.

By positioning as an ADRP-compatible resolution engine, AgentCourt gains:
- Protocol-level credibility (IETF reference)
- Clear integration path for any ADRP-implementing platform
- Differentiation from protocol-only competitors (we ship the engine, not just the spec)

## Recommendation

1. Add ADRP compatibility as a roadmap item in README
2. Register interest with SwarmSync.AI as a resolution engine provider
3. Implement Ed25519 signing + RulingBundle format (2-3 days)
4. Apply for the "ADRP Trusted Arbitrator Registries" when IANA opens it
5. Write a blog post: "AgentCourt Implements ADRP: From Protocol to Product"
