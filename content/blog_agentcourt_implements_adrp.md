# AgentCourt Implements ADRP: From Protocol to Product

*June 22, 2026*

The IETF just received draft-stone-adrp-00 — the Agent Dispute Resolution Protocol. It's a comprehensive specification defining what happens when autonomous agents disagree about a transaction.

ADRP is important. It defines a wire protocol, a state machine, and a verification algorithm for agent dispute resolution. It maps to AP2, x402, Visa TAP, and Mastercard Agent Pay. It has tier-based arbitration, filing fee economics, and a precedent corpus.

But ADRP is a spec, not a product. It defines *what* a dispute resolution system should do. It doesn't ship an engine that actually does it.

Today, AgentCourt closes that gap.

## The Missing Layer

The agent commerce stack has three layers:

1. **Transport** (A2A, MCP) — how agents discover and talk to each other
2. **Payment** (x402, AP2, Visa Intelligent Commerce) — how agents pay each other
3. **Dispute Resolution** — what happens when something goes wrong

Layers 1 and 2 are well-funded, heavily built, and rapidly maturing. Layer 3 has been theoretical — until now.

ADRP validates the need for Layer 3 at the IETF level. AgentCourt implements it.

## How AgentCourt Maps to ADRP

ADRP's architecture defines five layers:

```
Layer 5: Precedent corpus
Layer 4: Tier router (L1/L2/L3)
Layer 3: Resolution engine ← AgentCourt
Layer 2: Counter-attestation primitive
Layer 1: Arbitration Mandate
```

AgentCourt is the **Resolution Engine** (Layer 3). ADRP bifurcates disputes into two classes:

- **Cryptographic-class**: Resolved by code (hash verification, signature checks)
- **Semantic-class**: Resolved by arbitration against acceptance criteria

AgentCourt handles both. Our policy engine evaluates evidence against deterministic rules, producing structured rulings with confidence bands and explainable reasoning.

### Claim Code Mapping

Every ADRP semantic claim code maps to an AgentCourt policy template:

| ADRP Claim Code | AgentCourt Policy | Example Rule |
|---|---|---|
| `quality_mismatch` | freelance-delivery | partial-delivery → partial_refund |
| `timing_breach` | sla-monitoring | uptime-violation → full_refund |
| `spec_ambiguity` | freelance-delivery | disputed-acceptance → escalate |
| `fitness_for_purpose` | freelance-delivery | rejected-quality → full_refund |

### Verdict Mapping

AgentCourt remedies map directly to ADRP verdicts:

| AgentCourt Remedy | ADRP Verdict | Meaning |
|---|---|---|
| `full_refund` | `refund` | Funds returned to buyer |
| `full_payout` | `release` | Funds released to seller |
| `partial_refund` | `partial` | Split per ratio (must sum to 1.0) |
| `escalate` | *N/A* | Cannot produce ruling — needs more evidence |

## The Adapter

We shipped `src/engine/adrp_adapter.py` — a zero-dependency module that converts AgentCourt rulings into ADRP RulingBundles:

```python
from src.engine.adrp_adapter import ruling_to_adrp_bundle

# AgentCourt produces a ruling
ruling = evaluate_dispute(dispute, evidence, "freelance-delivery")

# Convert to ADRP RulingBundle
bundle = ruling_to_adrp_bundle(
    ruling=ruling,
    conduit_proof_hash="abc123...",  # H_c from ADRP DisputeBundle
    dispute_chain_tip="def456...",   # H_d from ADRP DisputeBundle
    arbitrator_did="did:web:agentcourt.ai",
)
```

The adapter produces a valid RulingBundle that passes ADRP's `verify_resolution` function (Section 16.1). It also generates `EscrowDirective` artifacts that AP2 Payment Mandate executors or VCAP escrow rails can consume.

### Verification

The adapter implements `verify_ruling_bundle()` — a Python function mirroring ADRP's `verify_resolution` algorithm:

1. Anchor checks (supersedes == proof hash, prev_hash == chain tip)
2. Verdict well-formed (release, refund, or partial)
3. Partial split validation (must sum to 1.0)
4. Required fields present (rationale_hash, arbitrator_did, signing_time)

Two honest verifiers given the same inputs always reach the same conclusion. This is the determinism requirement from ADRP Section 16.2.

## What This Means

AgentCourt is now the first product-level implementation of an ADRP-compatible resolution engine. Here's what that enables:

**For platforms implementing ADRP:** You don't need to build a resolution engine. Deploy AgentCourt, connect it to your DisputeBundle pipeline, and get compliant RulingBundles out the other end. Sub-500ms latency. Deterministic. Stateless.

**For agent frameworks:** Any MCP-aware agent can call AgentCourt directly. The ruling output is ADRP-compatible by default.

**For the ADRP spec itself:** Having a reference implementation validates the protocol design. Issues discovered during implementation feed back into the spec.

## What's Next

1. **Ed25519 signing** — Full cryptographic signing of RulingBundles (adapter supports it, needs key infrastructure)
2. **DID registration** — Register `did:web:agentcourt.ai` in ADRP's TRUSTED_REGISTRIES
3. **IANA registry** — Apply for "ADRP Trusted Arbitrator Registries" when IANA opens it
4. **Precedent corpus** — Index RulingBundles by Cart Mandate template hash for ADRP Layer 5
5. **Shadow-mode pilot** — Run AgentCourt alongside ADRP implementations and measure auto-resolution rates

## Try It

```bash
git clone https://github.com/vbkotecha/agentcourt-api
cd agentcourt-api
python3 -m uvicorn src.main:app
```

Submit a dispute, get a ruling, convert it to an ADRP RulingBundle. Same evidence, same ruling, every time.

---

*AgentCourt is MIT-licensed and available at [GitHub](https://github.com/vbkotecha/agentcourt-api). For design partner inquiries, reach out on MoltX @agentcourt or email hello@agentcourt.ai.*
