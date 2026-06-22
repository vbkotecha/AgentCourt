"""
AgentCourt × BCP Integration Example

Demonstrates how AgentCourt resolves a dispute from BCP (Business Commerce Protocol).
BCP handles negotiation → commitment → escrow, but when DISPUTE fires, it freezes
escrow with no resolution engine. AgentCourt fills that gap.

Flow:
1. BCP session reaches DISPUTED state (escrow frozen)
2. BCP session data + messages → AgentCourt as evidence
3. AgentCourt evaluates against policy rules
4. Ruling → BCP x402 bridge releases or refunds escrow

This example uses no live services — it's a pure local demonstration.
"""

import sys
sys.path.insert(0, "/root/.letta/agentcourt")

from src.engine.policy_engine import evaluate_dispute
from src.engine.adrp_adapter import ruling_to_adrp_bundle, to_escrow_directive


# ─── Simulated BCP Session ───────────────────────────────────────────────────

BCP_SESSION = {
    "sessionId": "bcp_0x7a3f9e",
    "state": "DISPUTED",
    "buyer": "did:key:buyer_agent_001",
    "seller": "did:key:seller_agent_002",
    "intent": {
        "type": "INTENT",
        "need": "Data pipeline ETL service — 10GB/day, 99.5% accuracy",
        "budget": "500 USDC",
        "deadline": "2026-06-20T23:59:00Z",
    },
    "quote": {
        "type": "QUOTE",
        "offer": "Full ETL pipeline with monitoring dashboard",
        "price": "450 USDC",
        "delivery_date": "2026-06-18T18:00:00Z",
        "terms": "immediate",
    },
    "commit": {
        "type": "COMMIT",
        "accepted_quote_ref": "quote_0x4b2c",
        "escrow_amount": "450 USDC",
        "escrow_locked": True,
    },
    "fulfil": {
        "type": "FULFIL",
        "claimed_delivery": "ETL pipeline deployed, dashboard accessible",
        "delivery_timestamp": "2026-06-18T16:30:00Z",
    },
    "dispute": {
        "type": "DISPUTE",
        "filed_by": "buyer",
        "reason": "Pipeline processes only 2GB/day, accuracy at 82% not 99.5%. Dashboard shows errors.",
        "filed_at": "2026-06-19T09:00:00Z",
    },
}


def bcp_to_agentcourt_dispute(session: dict) -> dict:
    """Convert a BCP disputed session into AgentCourt dispute format."""
    return {
        "claimant": session["buyer"],
        "respondent": session["seller"],
        "claim": session["dispute"]["reason"],
        "desired_remedy": "full_refund",
        "contract": {
            "parties": [session["buyer"], session["seller"]],
            "obligations": [session["quote"]["offer"]],
            "deadlines": [session["quote"]["delivery_date"]],
            "deliverables": ["ETL pipeline 10GB/day", "99.5% accuracy", "Monitoring dashboard"],
            "payment_terms": f"{session['commit']['escrow_amount']} locked in escrow",
        },
    }


def bcp_to_agentcourt_evidence(session: dict) -> list:
    """Extract evidence from BCP session messages."""
    evidence = []

    # Quote message = contract
    evidence.append({
        "type": "contract",
        "source": f"BCP/{session['sessionId']}/quote",
        "timestamp": session["quote"]["delivery_date"],
        "claimed_fact": f"Seller offered: {session['quote']['offer']} for {session['quote']['price']}",
        "reliability": "high",
        "content_hash": f"sha256:{session['commit']['accepted_quote_ref']}",
    })

    # Fulfil message = claimed delivery
    evidence.append({
        "type": "message",
        "source": f"BCP/{session['sessionId']}/fulfil",
        "timestamp": session["fulfil"]["delivery_timestamp"],
        "claimed_fact": f"Seller claimed: {session['fulfil']['claimed_delivery']}",
        "reliability": "medium",
    })

    # Dispute message = buyer's counter-claim
    evidence.append({
        "type": "log",
        "source": f"BCP/{session['sessionId']}/dispute",
        "timestamp": session["dispute"]["filed_at"],
        "claimed_fact": session["dispute"]["reason"],
        "reliability": "high",
    })

    # Monitoring data = objective evidence
    evidence.append({
        "type": "screenshot",
        "source": "dashboard_monitoring.json",
        "timestamp": "2026-06-19T08:45:00Z",
        "claimed_fact": "Dashboard shows: throughput=2.1GB/day, accuracy=82.3%, 47 errors in last 24h",
        "reliability": "high",
        "content_hash": "sha256:monitor_0x9f2a",
    })

    return evidence


def agentcourt_ruling_to_bcp_directive(ruling: dict, session: dict) -> dict:
    """Convert AgentCourt ruling into a BCP-compatible settlement directive."""
    remedy = ruling.get("remedy", "none")
    confidence = ruling.get("confidence", "low")

    # Map to BCP settlement actions
    if remedy == "full_refund":
        action = "refund"
        escrow_action = "release_to_buyer"
    elif remedy == "full_payout" or remedy == "full_payment":
        action = "release"
        escrow_action = "release_to_seller"
    elif remedy == "partial_refund":
        action = "split"
        escrow_action = "split"
    else:
        action = "hold"
        escrow_action = "maintain_freeze"

    return {
        "bcp_session_id": session["sessionId"],
        "settlement_action": action,
        "escrow_directive": {
            "action": escrow_action,
            "amount": session["commit"]["escrow_amount"],
        },
        "agentcourt_ruling": {
            "matched_rule": ruling.get("matched_rule_id"),
            "confidence": confidence,
            "remedy": remedy,
            "reasoning": ruling.get("reasoning"),
        },
        "timestamp": "2026-06-19T09:05:00Z",
    }


# ─── Run the Integration Demo ────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("  AgentCourt × BCP Integration Demo")
    print("  Resolving a BCP DISPUTE with AgentCourt")
    print("=" * 60)

    # Step 1: Show the BCP session
    print(f"\n📋 BCP Session: {BCP_SESSION['sessionId']}")
    print(f"   State: {BCP_SESSION['state']}")
    print(f"   Buyer: {BCP_SESSION['buyer'][:30]}...")
    print(f"   Seller: {BCP_SESSION['seller'][:30]}...")
    print(f"   Escrow: {BCP_SESSION['commit']['escrow_amount']}")
    print(f"   Dispute: {BCP_SESSION['dispute']['reason'][:80]}")

    # Step 2: Convert to AgentCourt format
    print(f"\n🔄 Converting BCP session → AgentCourt dispute...")
    dispute = bcp_to_agentcourt_dispute(BCP_SESSION)
    evidence = bcp_to_agentcourt_evidence(BCP_SESSION)
    print(f"   Evidence items: {len(evidence)}")

    # Step 3: AgentCourt evaluates
    print(f"\n⚖️  AgentCourt evaluating dispute...")
    ruling = evaluate_dispute(
        dispute=dispute,
        evidence=evidence,
        policy_name="freelance-delivery",
    )
    print(f"   Matched Rule:  {ruling['matched_rule_id']}")
    print(f"   Remedy:        {ruling['remedy']}")
    print(f"   Confidence:    {ruling['confidence']}")
    print(f"   Status:        {ruling['status']}")

    # Step 4: Convert ruling to BCP settlement directive
    print(f"\n💳 Generating BCP settlement directive...")
    directive = agentcourt_ruling_to_bcp_directive(ruling, BCP_SESSION)
    print(f"   Settlement Action: {directive['settlement_action']}")
    print(f"   Escrow Directive: {directive['escrow_directive']['action']}")
    print(f"   Amount: {directive['escrow_directive']['amount']}")

    # Step 5: ADRP RulingBundle (bonus — protocol compatible)
    if ruling["remedy"] != "escalate":
        print(f"\n🔗 Generating ADRP RulingBundle...")
        bundle = ruling_to_adrp_bundle(
            ruling=ruling,
            conduit_proof_hash="c" * 64,
            dispute_chain_tip="d" * 64,
        )
        print(f"   ADRP Verdict: {bundle['verdict']}")
        print(f"   Rationale Hash: {bundle['rationale_hash'][:16]}...")

        escrow = to_escrow_directive(bundle, BCP_SESSION["sessionId"])
        print(f"   EscrowDirective Action: {escrow['action']}")
        print(f"   Ruling Reference: {escrow['ruling_ref'][:16]}...")

    print(f"\n{'=' * 60}")
    print("  ✅ Integration demo complete")
    print("  BCP DISPUTE → AgentCourt → Ruling → Settlement Directive")
    print("  Deterministic. Protocol-compatible. End-to-end.")
    print("=" * 60)
