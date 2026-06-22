"""
AgentCourt x402 Payment Middleware

Enables AgentCourt API to be discovered and called by AI agents using
AgentCash, Coinbase x402, or any x402-compatible client.

When an agent calls a paid endpoint without payment:
1. API returns HTTP 402 with payment requirements
2. Agent signs USDC payment on Base
3. Agent retries with X-Payment header
4. Middleware verifies payment → allows request through

Usage:
    from x402_middleware import X402Middleware
    app.add_middleware(X402Middleware, price_usdc=0.05, wallet_address=WALLET)

Price: $0.05 per dispute resolution call
Free endpoints: /health, /docs, /openapi.json, /, /policies
"""

import os
import json
import hashlib
import time
from urllib.parse import parse_qs, urlparse


class X402Config:
    """Configuration for x402 payment middleware."""

    def __init__(
        self,
        price_usdc: float = 0.05,
        wallet_address: str = None,
        chain: str = "base-mainnet",
        currency: str = "USDC",
        free_paths: list = None,
    ):
        self.price_usdc = price_usdc
        self.wallet_address = wallet_address or os.getenv("AGENTCOURT_WALLET_ADDRESS", "")
        self.chain = chain
        self.currency = currency
        self.free_paths = free_paths or [
            "/health",
            "/docs",
            "/openapi.json",
            "/openapi.yaml",
            "/redoc",
            "/",
            "/policies",
            "/policies/",
            "/api-docs",
            "/swagger",
            "/demos",
            "/verdicts",
        ]


class PaymentVerifier:
    """
    Verifies x402 payments.

    In production, this would verify on-chain USDC transfers.
    For now, implements a simplified verification that checks:
    1. Payment header exists and is valid JSON
    2. Amount matches required price
    3. Recipient matches wallet address
    4. Payment hasn't been used before (replay protection)
    """

    def __init__(self, wallet_address: str):
        self.wallet_address = wallet_address
        self._used_payments = set()  # Simple replay protection

    def verify(self, payment_header: str, required_amount: float) -> tuple:
        """
        Verify a payment header.
        Returns (is_valid: bool, error: str or None)
        """
        if not payment_header:
            return False, "No payment header provided"

        try:
            # Decode payment (in production, this would be a signed transaction)
            # Format: base64url(JSON{amount, currency, chain, recipient, tx_hash, signature})
            import base64
            decoded = base64.urlsafe_b64decode(payment_header + "==")
            payment = json.loads(decoded)
        except Exception:
            return False, "Invalid payment format"

        # Check amount
        amount = float(payment.get("amount", 0))
        if amount < required_amount:
            return False, f"Insufficient payment: {amount} < {required_amount}"

        # Check currency
        if payment.get("currency", "").upper() != "USDC":
            return False, "Only USDC accepted"

        # Check recipient
        recipient = payment.get("recipient", "")
        if recipient != self.wallet_address:
            return False, "Wrong recipient address"

        # Check chain
        chain = payment.get("chain", "")
        if chain not in ("base-mainnet", "base", "8453"):
            return False, "Only Base network supported"

        # Replay protection
        tx_hash = payment.get("tx_hash", "")
        if tx_hash in self._used_payments:
            return False, "Payment already used"
        self._used_payments.add(tx_hash)

        # In production: verify on-chain via Coinbase x402 facilitator
        # from coinbase_x402 import Facilitator
        # facilitator = Facilitator()
        # return facilitator.verify(payment_header, required_amount)

        return True, None


def generate_402_response(required_amount: float, config: X402Config):
    """Generate a standard x402 Payment Required response body."""
    return {
        "error": "Payment Required",
        "x402_version": 1,
        "payment_required": {
            "amount": str(required_amount),
            "currency": config.currency,
            "chain": config.chain,
            "recipient": config.wallet_address,
            "description": "AgentCourt dispute resolution",
            "accepted_networks": ["base-mainnet"],
        },
        "instructions": (
            "Pay the required USDC amount to the recipient address on Base. "
            "Include the payment proof in the X-Payment header as base64url(JSON). "
            "See https://x402.org for protocol details."
        ),
    }


def get_openapi_payment_annotations():
    """
    Returns x-payment-info annotations for OpenAPI spec.
    These tell AgentCash and other x402 clients about pricing.
    """
    return {
        "/v1/disputes": {
            "post": {
                "x-payment-info": {
                    "price": "0.05",
                    "currency": "USDC",
                    "chain": "base-mainnet",
                    "network": "base",
                    "description": "Resolve a single dispute with policy engine",
                }
            }
        },
        "/v1/disputes/batch": {
            "post": {
                "x-payment-info": {
                    "price": "0.40",
                    "currency": "USDC",
                    "chain": "base-mainnet",
                    "network": "base",
                    "description": "Resolve up to 10 disputes in batch",
                }
            }
        },
        "/v1/verdicts/{case_id}": {
            "get": {
                "x-payment-info": {
                    "price": "0.01",
                    "currency": "USDC",
                    "chain": "base-mainnet",
                    "network": "base",
                    "description": "Look up a previous verdict by case ID",
                }
            }
        },
    }


def get_discovery_spec():
    """
    Returns a /.well-known/x402 discovery document.
    This is what AgentCash looks for to index the API.
    """
    wallet = os.getenv("AGENTCOURT_WALLET_ADDRESS", "")
    return {
        "x402_version": 1,
        "server": "AgentCourt",
        "description": "Policy-driven dispute resolution for agent commerce",
        "endpoints": {
            "/v1/disputes": {
                "method": "POST",
                "price": "0.05 USDC",
                "description": "Resolve a dispute with evidence and policy rules",
            },
            "/v1/disputes/batch": {
                "method": "POST",
                "price": "0.40 USDC",
                "description": "Resolve up to 10 disputes",
            },
            "/v1/verdicts/{case_id}": {
                "method": "GET",
                "price": "0.01 USDC",
                "description": "Look up a verdict",
            },
            "/v1/policies": {
                "method": "GET",
                "price": "Free",
                "description": "List available policy templates",
            },
        },
        "payment": {
            "methods": ["x402"],
            "currency": "USDC",
            "chain": "base-mainnet",
            "recipient": wallet,
        },
        "discovery_docs": ["/openapi.json", "/.well-known/x402"],
    }
