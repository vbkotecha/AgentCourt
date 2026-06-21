"""
x402 Payment Integration for AgentCourt API

This module adds per-ruling micropayments to the AgentCourt dispute resolution API.
Agents pay $0.50-$5.00 per ruling using USDC on Base via the x402 protocol.

Payment schemes:
- Simple disputes: $0.50 (exact)
- Standard disputes: $2.00 (exact)
- Complex disputes with evidence: $5.00 (exact)
- Usage-based (upto): max $5.00, settle based on complexity

Architecture:
1. Client sends dispute request
2. Server responds with HTTP 402 + payment requirements
3. Client pays via x402 (USDC on Base)
4. Server processes dispute after payment confirmed
5. Returns ruling

For now, this is a reference implementation. The actual x402 middleware
needs to be deployed on the AgentCourt Railway service.
"""

# x402 payment configuration for AgentCourt
X402_CONFIG = {
    "facilitator_url": "https://x402.org/facilitator",  # testnet; use production facilitator for mainnet
    "network": "base",  # Base mainnet for production
    "currency": "USDC",
    "wallet_address": "0x...",  # AgentCourt receiving wallet (needs to be set)
    "pricing": {
        "/dispute": {
            "simple": {"price": "$0.50", "scheme": "exact"},
            "standard": {"price": "$2.00", "scheme": "exact"},
            "complex": {"price": "$5.00", "scheme": "exact"},
            "usage_based": {"price": "up to $5.00", "scheme": "upto"},
        },
        "/cases": {"price": "free", "scheme": "none"},
        "/cases/{case_id}": {"price": "free", "scheme": "none"},
        "/health": {"price": "free", "scheme": "none"},
    },
}

# Next.js / FastAPI middleware integration
# For FastAPI (AgentCourt's stack):

MIDDLEWARE_CODE = """
from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

class X402PaymentMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Skip payment for free endpoints
        if request.url.path in ["/health", "/cases", "/docs", "/openapi.json"]:
            return await call_next(request)
        
        # For /dispute endpoint, check for payment header
        if request.url.path == "/dispute":
            payment_header = request.headers.get("X-Payment", "")
            
            # If no payment, return 402 with payment requirements
            if not payment_header:
                return Response(
                    content=json.dumps({
                        "error": "payment_required",
                        "payment": {
                            "version": 1,
                            "network": "base",
                            "asset": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",  # USDC on Base
                            "amount": "2000000",  # $2.00 in USDC (6 decimals)
                            "recipient": WALLET_ADDRESS,
                            "scheme": "exact",
                        }
                    }),
                    status_code=402,
                    media_type="application/json",
                    headers={
                        "X-Payment-Version": "1",
                        "X-Payment-Network": "base",
                        "X-Payment-Asset": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
                        "X-Payment-Amount": "2000000",
                        "X-Payment-Recipient": WALLET_ADDRESS,
                        "X-Payment-Scheme": "exact",
                    }
                )
            
            # If payment present, verify via facilitator
            # TODO: Implement facilitator verification
            # For now, trust the payment header
        
        return await call_next(request)
"""

# Python buyer client for agents wanting to use AgentCourt
BUYER_CLIENT_CODE = """
# For agents that want to call AgentCourt with x402 payments
# pip install x402-requests

import requests
from x402.requests import wrap_session_with_payment
from x402.evm import EVMClient

# Set up wallet
evm_client = EVMClient(
    private_key="your_private_key",
    rpc_url="https://mainnet.base.org",
)

# Wrap requests session with x402 payment handling
session = requests.Session()
wrap_session_with_payment(session, evm_client)

# Now make paid requests to AgentCourt
response = session.post(
    "https://agentcourt-api-production.up.railway.app/dispute",
    json={
        "claimant": "AgentA",
        "respondent": "AgentB",
        "claim": "AgentB delivered late",
        "desired_remedy": "Partial refund of $100 USDC",
    }
)

# Payment is handled automatically
ruling = response.json()
print(ruling["ruling"])
"""

# Implementation status
STATUS = """
CURRENT STATE:
- x402 payment protocol researched and documented
- Pricing model defined ($0.50-$5.00 per ruling)
- Middleware reference code written
- Buyer client reference code written

NEXT STEPS:
1. Set up AgentCourt wallet on Base (needs Vivek's wallet or new one)
2. Install x402 Python SDK on AgentCourt Railway service
3. Add payment middleware to FastAPI app
4. Test on Base Sepolia (testnet)
5. Deploy to Base mainnet
6. Register AgentCourt on x402 Bazaar for discoverability

BLOCKERS:
- Need wallet address for receiving payments
- Need to deploy updated AgentCourt code to Railway
- x402 Python SDK may need to be installed via pip
"""

if __name__ == "__main__":
    print("x402 Integration Reference for AgentCourt")
    print("=" * 50)
    print(f"Network: {X402_CONFIG['network']}")
    print(f"Currency: {X402_CONFIG['currency']}")
    print(f"Pricing:")
    for endpoint, tiers in X402_CONFIG["pricing"].items():
        if isinstance(tiers, dict) and "price" not in tiers:
            for tier, details in tiers.items():
                print(f"  {endpoint} ({tier}): {details['price']} ({details['scheme']})")
        else:
            print(f"  {endpoint}: {tiers.get('price', 'N/A')}")
