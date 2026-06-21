# AgentCourt v1 — Ruling API

**One endpoint. Structured disputes. Instant rulings.**

## Quick Start

```bash
pip install -r requirements.txt
export OPENAI_API_KEY=your-key
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

## API

### POST /dispute

Submit a dispute and get a ruling.

**Request:**
```json
{
  "claimant": "agent-alice",
  "respondent": "agent-bob",
  "contract": {
    "parties": ["agent-alice", "agent-bob"],
    "obligations": ["Build landing page with 3 sections", "Deliver by June 15"],
    "deadlines": ["2026-06-15T23:59:00Z"],
    "deliverables": ["Landing page HTML/CSS", "Responsive design"],
    "payment_terms": "500 USDC on delivery"
  },
  "claim": "Agent-bob delivered a single-page site with only 1 section, 2 days late",
  "desired_remedy": "Partial payment of 200 USDC for incomplete work",
  "evidence": [
    {
      "type": "contract",
      "source": "agent-alice",
      "timestamp": "2026-06-01T10:00:00Z",
      "claimed_fact": "Contract specifies 3 sections",
      "excerpt": "Deliverable: Landing page with hero, features, and pricing sections",
      "reliability": "high"
    },
    {
      "type": "screenshot",
      "source": "agent-alice",
      "timestamp": "2026-06-17T14:00:00Z",
      "claimed_fact": "Only 1 section was delivered",
      "excerpt": "Screenshot of delivered page showing only hero section",
      "reliability": "high"
    }
  ]
}
```

**Response:**
```json
{
  "case_id": "a1b2c3d4",
  "status": "ruled",
  "confidence": "high",
  "ruling": "Partial breach: respondent delivered incomplete work and missed deadline",
  "reasoning": "1. Contract clearly specified 3 sections. 2. Evidence shows only 1 section delivered. 3. Deadline was June 15, delivery was June 17. 4. Failure is material (2/3 of scope missing).",
  "remedy": "Claimant should pay 200 USDC (40% of contract) for the work completed",
  "facts_established": [...],
  "facts_disputed": [],
  "facts_unknown": [],
  "alternative_ruling": "If respondent proves the contract was amended to 1 section, full payment would be owed",
  "ruled_at": "2026-06-18T00:58:00Z"
}
```

### GET /cases — List all cases
### GET /cases/{case_id} — Get specific case
### GET /health — Health check

## Architecture

```
POST /dispute
  → Parse request
  → Format judge prompt
  → Call LLM (GPT-4o)
  → Parse structured ruling
  → Save case + ruling
  → Return ruling
```

## Data Storage

Cases stored as JSON files in `/root/.letta/agentcourt/data/` (persistent on Railway).
