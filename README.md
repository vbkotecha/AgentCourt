# AgentCourt

**The dispute layer for agent commerce.**

Submit evidence. Apply policy rules. Get a ruling. No escrow, no courtroom theater.

## Live API

**Base URL:** `https://agentcourt-api-production.up.railway.app`
**Docs:** `https://agentcourt-api-production.up.railway.app/docs`

## Quick Start

```python
from agentcourt import AgentCourt

court = AgentCourt()

ruling = court.dispute(
    claimant="ClientCorp",
    respondent="DevStudio",
    contract={
        "obligations": ["Build mobile app"],
        "deadlines": ["2026-07-01T23:59:00Z"],
        "deliverables": ["iOS app", "Android app"],
    },
    claim="Developer never delivered the app",
    desired_remedy="Full refund of deposit",
    policy="freelance-delivery",
    evidence=[
        {
            "type": "contract",
            "source": "ClientCorp",
            "timestamp": "2026-06-01T10:00:00Z",
            "claimed_fact": "Signed contract, no deliverable received",
            "reliability": "high",
        }
    ],
)

print(ruling.confidence)  # high
print(ruling.remedy)      # full_refund
print(ruling.ruling)      # The respondent failed to deliver...
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/v1/disputes` | Submit a dispute, get a ruling |
| `GET` | `/v1/cases` | List all cases |
| `GET` | `/v1/cases/{id}` | Get a specific case |
| `GET` | `/v1/policies` | List policy templates |
| `GET` | `/v1/policies/{name}` | Get policy details |
| `GET` | `/health` | API health check |
| `GET` | `/docs` | Interactive API docs (Swagger) |

## Policy Templates

### freelance-delivery
Disputes over digital work delivery: non-delivery, late delivery, scope issues.

**Rules:** non-delivery, late-delivery-accepted, late-delivery-rejected, partial-delivery, default-no-match

### milestone-payment  
Disputes over milestone payments: unpaid milestones, overdue payments, partial payments.

**Rules:** milestone-completed-unpaid, milestone-completed-paid-on-time, milestone-incomplete-payment-justified, milestone-overdue-disputed, default-no-match

### bug-bounty
Disputes over bug bounty claims: reproducibility, severity, disclosure compliance.

**Rules:** valid-bug-full-payout, non-reproducible-bug, severity-below-threshold, non-compliant-disclosure, default-no-match

## How It Works

1. **Submit evidence** — contracts, commits, logs, screenshots, payment records
2. **Evidence scoring** — each item weighted by type, reliability, recency, and hash verification
3. **Fact extraction** — structured facts derived from evidence + metadata
4. **Policy matching** — facts evaluated against policy rules (deterministic)
5. **Confidence band** — high/medium/low based on evidence quality and fact completeness
6. **Ruling generated** — with remedy, full audit trail, and explainable reasoning

## Key Design Decisions

- **No escrow required** — rulings create consequences through reputation and enforcement, not custody
- **Deterministic** — same evidence + policy always produces the same ruling
- **Explainable** — every ruling shows which rule matched, which facts were established, and evidence scores
- **Policy-first** — define rules upfront, not case-by-case
- **API-first** — REST + SDK, integrate in minutes

## SDK

```bash
pip install agentcourt  # coming soon
```

Or copy `sdk/agentcourt.py` — zero dependencies, standard library only.

## Architecture

```
src/
├── main.py              # FastAPI app with REST endpoints
├── engine/
│   └── policy_engine.py # Deterministic rule evaluation engine
└── policies/
    ├── freelance-delivery.json
    ├── milestone-payment.json
    └── bug-bounty.json
```

## License

MIT
