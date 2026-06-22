# AgentCourt on AgentCash — Reverse Integration Plan

## The Insight

We don't need a partnership meeting with Merit Systems to get AgentCourt in front of every AgentCash user. We can **publish AgentCourt as a paid x402 API** and agents will discover it automatically.

AgentCash indexes APIs that publish OpenAPI documents at `/openapi.json` with `x-payment-info` annotations. Any agent using AgentCash can then `search("dispute resolution")` and find AgentCourt.

## How It Works

### Step 1: Add x402 Payment to AgentCourt API

Add a 402 payment interceptor to the AgentCourt FastAPI app:

```python
@app.middleware("http")
async def x402_paywall(request: Request, call):
    # Skip health, docs, swagger
    if request.url.path in ["/health", "/docs", "/openapi.json"]:
        return await call(request)

    # Check for payment header
    payment = request.headers.get("X-Payment")
    if payment:
        # Verify USDC payment on Base
        if verify_payment(payment, amount=0.05):
            return await call(request)

    # Return 402
    return JSONResponse(
        status_code=402,
        content={
            "error": "Payment required",
            "amount": "0.05",
            "currency": "USDC",
            "chain": "base",
            "recipient": AGENTCOURT_WALLET_ADDRESS,
        }
    )
```

### Step 2: Publish Discovery Spec

Add `x-payment-info` annotations to AgentCourt's OpenAPI spec:

```json
{
  "paths": {
    "/v1/disputes": {
      "post": {
        "summary": "Resolve a dispute",
        "x-payment-info": {
          "price": "0.05",
          "currency": "USDC",
          "chain": "base",
          "network": "base-mainnet"
        }
      }
    }
  }
}
```

### Step 3: Register on x402scan.com

Submit AgentCourt's API endpoint to x402scan.com and mppscan.com for indexing.

### Step 4: Agents Discover Automatically

Any agent using AgentCash can now:
```
agent.search("dispute resolution") → finds AgentCourt
agent.fetch("https://api.agentcourt.ai/v1/disputes", ...) → pays $0.05 → gets ruling
```

## Business Model

| Call Type | Price | Volume Est (3mo) | Revenue |
|-----------|-------|------------------|---------|
| Single dispute resolution | $0.05 | 1,000/month | $50/mo |
| Batch dispute (10+) | $0.40 | 200/month | $80/mo |
| Policy template listing | $0.02 | 5,000/month | $100/mo |
| Verdict lookup | $0.01 | 10,000/month | $100/mo |

**Conservative 3-month revenue: ~$330/month** from AgentCash distribution alone.

More importantly: **every paid call is a customer**. Once agents are calling AgentCourt, we have usage data, customer relationships, and revenue proof.

## Why This Is Better Than Waiting for a Partnership

1. **Zero meetings needed** — Just publish and register
2. **Immediate distribution** — 921K+ AgentCash calls/month, growing 246%
3. **Self-serve** — Agents discover via search, no sales cycle
4. **Revenue from day 1** — $0.05/dispute, paid in USDC
5. **Validates demand** — If agents call it, we have product-market fit proof
6. **Strengthens partnership pitch** — "We already have X disputes resolved through AgentCash" is a much stronger opening than "we'd like to integrate"

## Implementation Steps

1. **Create AgentCourt wallet** on Base (USDC recipient)
2. **Add x402 middleware** to FastAPI (intercept, verify, allow)
3. **Annotate OpenAPI spec** with `x-payment-info`
4. **Register on x402scan.com** and mppscan.com
5. **Test with AgentCash CLI** — `agentcash fetch https://api.agentcourt.ai/v1/disputes`
6. **Monitor** — watch for first paid calls

## Timeline

- **Day 1-2:** Add x402 middleware + wallet + OpenAPI annotations (after API is deployed)
- **Day 3:** Register on x402scan.com, test with AgentCash CLI
- **Day 4:** First agents discover AgentCourt via search
- **Week 2:** First paid dispute resolution calls
- **Month 1:** Partnership conversation with Merit Systems (backed by real usage data)

---

*This is the fastest path to market. No gatekeepers. No sales cycle. Just publish and let agents find us.*
