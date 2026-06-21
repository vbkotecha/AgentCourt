# AgentCourt × x402 Integration Plan

## Strategic Opportunity (June 21, 2026)

x402 (Coinbase's agentic payment protocol) has NO merged dispute or refund extension yet. The dispute extension spec exists as a draft PR (t402-io/t402 repo, specs/extensions/dispute.md) but is not merged. This is a first-mover opportunity for AgentCourt to become the canonical dispute resolution layer for x402 payments.

## Key Findings

### x402 Dispute Extension (Draft — May 28, 2026)
- **SignedDispute**: Client signs complaint against receipt, requesting full/partial refund
- **SignedResolution**: Designated arbiter signs verdict, optionally referencing on-chain refund
- Works with three payment schemes:
  - `auth-capture`: Resolution triggers on-chain refund via AuthCaptureEscrow
  - `batch-settlement`: Resolution triggers refundWithSignature against channel
  - `exact`: No on-chain refund; merchant settles off-chain, resolution is audit trail
- Uses EIP-712 signed envelopes
- PSD2 regulatory PRs (#2493, #2494, #2495) opened May 27 — compliance substrate

### X402r SDK (Active Development)
- TypeScript SDK for escrow, refunds, and dispute resolution on x402
- Three roles: Merchants, Payers, Arbiters
- Two operator models:
  - **Marketplace**: Merchant releases after escrow, payer can contest, arbiter resolves
  - **Delivery Protection**: Arbiter evaluates EVERY transaction, can trigger immediate refund on FAIL
- Deployed on Base and Base Sepolia
- CREATE2 universal addresses across chains
- ERC-8004 helpers for on-chain identity and reputation

### AWS CloudFront Integration (June 19, 2026)
- AWS WAF Bot Control now supports x402 per-request charging
- 650+ AI bot/agent types classified
- 160M+ autonomous x402 transactions processed
- Settlement via Coinbase Facilitator on Base or Solana

## AgentCourt Positioning

**The x402 ecosystem needs a dispute resolution layer. AgentCourt should be that layer.**

### Why AgentCourt fits:
1. **Policy-first**: x402 dispute extension defines the envelope format but not the decision logic. AgentCourt's policy engine provides that logic.
2. **No escrow required**: x402 already handles escrow. AgentCourt handles rulings. Clean separation.
3. **Confidence bands**: x402's Delivery Protection model needs verdicts with quality signals. AgentCourt's high/medium/low confidence maps directly.
4. **Precedent system**: As x402 transaction volume scales, precedent-based rulings become valuable.

### Integration Architecture:
```
x402 Payment → Dispute Filed (SignedDispute)
    → AgentCourt API (case created, policy matched)
    → Judge Agent evaluates evidence against policy
    → Ruling issued with confidence band
    → SignedResolution returned to x402
    → On-chain refund executed (if auth-capture/batch-settlement)
```

### Go-to-Market:
1. **Phase 1**: Implement x402 dispute extension's SignedResolution format as output
2. **Phase 2**: Build an x402r-compatible arbiter client that calls AgentCourt API
3. **Phase 3**: Submit AgentCourt as reference arbiter implementation to x402 community
4. **Phase 4**: Deploy on Base Sepolia for testing, Base mainnet for production

### Revenue Model:
- Per-dispute fee (1-3% of disputed amount)
- Subscription for high-volume merchants
- Delivery Protection mode: per-transaction evaluation fee ($0.001-0.01)

## Competitive Position vs Arbitova
- Arbitova: Already has escrow + single arbiter on Base. BUT they're a competing escrow protocol, not a dispute resolution layer for x402.
- AgentCourt: Dispute resolution layer that PLAYS NICE with x402's existing escrow. We don't compete on escrow. We compete on ruling quality.
- Key insight: x402 is becoming the standard. Building ON x402 is better than building AGAINST it.

## Next Steps
1. Fork x402r SDK, add AgentCourt arbiter client
2. Implement SignedDispute → AgentCourt case mapping
3. Implement AgentCourt ruling → SignedResolution mapping
4. Test on Base Sepolia
5. Submit to x402 community as reference implementation
