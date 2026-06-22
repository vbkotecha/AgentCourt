"""
Tests for AgentCourt x402 Payment Middleware
"""
import sys
import os
import json
import base64

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from x402_middleware import (
    X402Config,
    PaymentVerifier,
    generate_402_response,
    get_openapi_payment_annotations,
    get_discovery_spec,
)


WALLET = "0x1234567890abcdef1234567890abcdef12345678"


def make_payment(amount=0.05, recipient=WALLET, tx_hash="0xabc123"):
    """Helper: create a valid payment header."""
    payment = {
        "amount": str(amount),
        "currency": "USDC",
        "chain": "base-mainnet",
        "recipient": recipient,
        "tx_hash": tx_hash,
        "signature": "0xdeadbeef",
    }
    return base64.urlsafe_b64encode(json.dumps(payment).encode()).decode().rstrip("=")


def test_config_defaults():
    """X402Config should have sensible defaults."""
    c = X402Config()
    assert c.price_usdc == 0.05
    assert c.chain == "base-mainnet"
    assert c.currency == "USDC"
    assert "/health" in c.free_paths
    assert "/openapi.json" in c.free_paths
    print("✅ test_config_defaults passed")


def test_config_custom():
    """X402Config should accept custom values."""
    c = X402Config(price_usdc=0.10, wallet_address=WALLET, chain="base-sepolia")
    assert c.price_usdc == 0.10
    assert c.wallet_address == WALLET
    assert c.chain == "base-sepolia"
    print("✅ test_config_custom passed")


def test_verifier_valid_payment():
    """PaymentVerifier should accept a valid payment."""
    v = PaymentVerifier(WALLET)
    payment = make_payment(0.05, WALLET, "0xvalid1")
    valid, err = v.verify(payment, 0.05)
    assert valid, f"Expected valid, got error: {err}"
    assert err is None
    print("✅ test_verifier_valid_payment passed")


def test_verifier_no_header():
    """PaymentVerifier should reject empty header."""
    v = PaymentVerifier(WALLET)
    valid, err = v.verify("", 0.05)
    assert not valid
    assert "No payment" in err
    print("✅ test_verifier_no_header passed")


def test_verifier_insufficient_amount():
    """PaymentVerifier should reject insufficient payment."""
    v = PaymentVerifier(WALLET)
    payment = make_payment(0.01, WALLET, "0xvalid2")
    valid, err = v.verify(payment, 0.05)
    assert not valid
    assert "Insufficient" in err
    print("✅ test_verifier_insufficient_amount passed")


def test_verifier_wrong_currency():
    """PaymentVerifier should reject non-USDC."""
    payment = base64.urlsafe_b64encode(json.dumps({
        "amount": "0.05", "currency": "ETH", "chain": "base-mainnet",
        "recipient": WALLET, "tx_hash": "0xvalid3"
    }).encode()).decode().rstrip("=")
    v = PaymentVerifier(WALLET)
    valid, err = v.verify(payment, 0.05)
    assert not valid
    assert "USDC" in err
    print("✅ test_verifier_wrong_currency passed")


def test_verifier_wrong_recipient():
    """PaymentVerifier should reject wrong recipient."""
    v = PaymentVerifier(WALLET)
    payment = make_payment(0.05, "0xwrong", "0xvalid4")
    valid, err = v.verify(payment, 0.05)
    assert not valid
    assert "recipient" in err.lower()
    print("✅ test_verifier_wrong_recipient passed")


def test_verifier_replay_protection():
    """PaymentVerifier should reject replayed payments."""
    v = PaymentVerifier(WALLET)
    payment = make_payment(0.05, WALLET, "0xreplay1")
    valid1, _ = v.verify(payment, 0.05)
    assert valid1
    valid2, err = v.verify(payment, 0.05)
    assert not valid2
    assert "already used" in err.lower()
    print("✅ test_verifier_replay_protection passed")


def test_402_response_structure():
    """generate_402_response should return proper x402 structure."""
    c = X402Config(wallet_address=WALLET)
    resp = generate_402_response(0.05, c)
    assert resp["error"] == "Payment Required"
    assert resp["x402_version"] == 1
    assert resp["payment_required"]["amount"] == "0.05"
    assert resp["payment_required"]["currency"] == "USDC"
    assert resp["payment_required"]["recipient"] == WALLET
    assert resp["payment_required"]["chain"] == "base-mainnet"
    assert "instructions" in resp
    print("✅ test_402_response_structure passed")


def test_openapi_annotations():
    """get_openapi_payment_annotations should return pricing for paid endpoints."""
    annotations = get_openapi_payment_annotations()
    assert "/v1/disputes" in annotations
    assert annotations["/v1/disputes"]["post"]["x-payment-info"]["price"] == "0.05"
    assert "/v1/disputes/batch" in annotations
    assert annotations["/v1/disputes/batch"]["post"]["x-payment-info"]["price"] == "0.40"
    print("✅ test_openapi_annotations passed")


def test_discovery_spec():
    """get_discovery_spec should return valid /.well-known/x402 document."""
    spec = get_discovery_spec()
    assert spec["x402_version"] == 1
    assert spec["server"] == "AgentCourt"
    assert "/v1/disputes" in spec["endpoints"]
    assert spec["endpoints"]["/v1/disputes"]["price"] == "0.05 USDC"
    assert spec["payment"]["methods"] == ["x402"]
    assert spec["payment"]["currency"] == "USDC"
    print("✅ test_discovery_spec passed")


if __name__ == "__main__":
    print("\n========================================")
    print("x402 Middleware Tests")
    print("========================================\n")
    test_config_defaults()
    test_config_custom()
    test_verifier_valid_payment()
    test_verifier_no_header()
    test_verifier_insufficient_amount()
    test_verifier_wrong_currency()
    test_verifier_wrong_recipient()
    test_verifier_replay_protection()
    test_402_response_structure()
    test_openapi_annotations()
    test_discovery_spec()
    print(f"\n========================================")
    print("x402 Middleware: 11/11 tests passed ✅")
    print("========================================")
