# AgentCourt M1 Build Plan — Judge Agent + Ruling Engine

## Goal
Ship the first production-grade version of AgentCourt as a **policy-first dispute resolution API** with:
- **No escrow in v1**
- **Evidence-native inputs** with structured provenance
- **Confidence bands** on every ruling (`high`, `medium`, `low`)
- **FastAPI REST API** deployable on **Railway**
- Three starter policy templates:
  - `freelance-delivery`
  - `milestone-payment`
  - `bug-bounty`

## Assumptions
- I could not directly inspect the referenced `consulatehq_strategy.md` file in this workspace, so this plan is based on the AgentCourt API spec, the current `src/main.py`, and the adjacent launch/distribution docs.
- M1 focuses on the judge agent + deterministic ruling engine, not escrow, human arbitration, appeals, precedent search, or on-chain enforcement.
- Payment enforcement, if any, is **external/advisory** in M1; AgentCourt does not custody funds.

---

## 1) Exact file structure to create

```text
/root/.letta/agentcourt/
├── src/
│   ├── main.py                        # Thin FastAPI bootstrap for Railway / uvicorn
│   ├── app/
│   │   ├── __init__.py
│   │   ├── server.py                  # FastAPI app factory + router registration
│   │   ├── settings.py                # Env vars, paths, defaults, feature flags
│   │   └── deps.py                    # Shared dependencies (repo, catalog, engine)
│   ├── api/
│   │   ├── __init__.py
│   │   ├── health.py                  # /health
│   │   ├── cases.py                   # /cases, /cases/{id}
│   │   ├── evidence.py                # /cases/{id}/evidence
│   │   ├── policies.py                # /policies, /policies/{id}
│   │   ├── templates.py               # /templates, /templates/{id}/apply
│   │   └── rulings.py                 # /cases/{id}/ruling
│   ├── models/
│   │   ├── __init__.py
│   │   ├── common.py                  # Party, metadata, enums
│   │   ├── evidence.py                # EvidenceItem, provenance, reliability
│   │   ├── policy.py                  # Policy, Rule, Template, parameters
│   │   ├── case.py                    # Case, claim, status transitions
│   │   └── ruling.py                  # Ruling, reasoning, consequences, confidence
│   ├── engine/
│   │   ├── __init__.py
│   │   ├── canonicalize.py            # Normalize input case/evidence to a canonical form
│   │   ├── evidence_score.py          # Score evidence strength and trust
│   │   ├── policy_compiler.py         # Compile YAML/JSON template into executable rule AST
│   │   ├── predicate_eval.py          # Safe predicate evaluator for rule conditions
│   │   ├── confidence.py              # Map support/conflict into high/medium/low
│   │   └── ruling_engine.py           # Orchestrates end-to-end ruling
│   ├── storage/
│   │   ├── __init__.py
│   │   ├── repository.py              # Abstract repository interface
│   │   ├── sqlite_repo.py             # M1 persistence on Railway
│   │   └── migrations/                # Schema/versioning for SQLite tables
│   ├── templates/
│   │   ├── freelance-delivery.yaml     # Policy template source
│   │   ├── milestone-payment.yaml
│   │   └── bug-bounty.yaml
│   ├── schemas/
│   │   ├── evidence.schema.json       # Validation schema for evidence-native inputs
│   │   ├── policy-template.schema.json # Validation schema for policy templates
│   │   └── ruling.schema.json         # Validation schema for output rulings
│   └── utils/
│       ├── __init__.py
│       ├── ids.py                     # Stable IDs and prefixes
│       └── time.py                    # ISO-8601 helpers
├── tests/
│   ├── test_evidence_scoring.py
│   ├── test_policy_compiler.py
│   ├── test_ruling_engine.py
│   └── test_api.py
├── Dockerfile
├── railway.toml
├── requirements.txt
└── README.md                          # Optional if you need deployment/run instructions
```

### Notes on the current `src/main.py`
- Keep it, but reduce it to a thin bootstrap:
  - load env
  - import `app` from `src.app.server`
  - expose `app` for `uvicorn src.main:app`
- Move all business logic out of the monolith into the modules above.

---

## 2) Core modules and responsibilities

| Module | Responsibility |
|---|---|
| `src/app/server.py` | Create the FastAPI app, register routers, middleware, OpenAPI tags, and startup hooks. |
| `src/app/settings.py` | Centralized config: `PORT`, `DATA_DIR`, `DATABASE_URL` (optional), `JUDGE_MODEL`, `POLICY_DIR`, `ENV`. |
| `src/models/evidence.py` | Evidence-native schema with `type`, `source`, `hash`, `claimed_fact`, `reliability_score`, timestamps, and optional provenance fields. |
| `src/models/policy.py` | Policy template object, rule definitions, parameters, confidence bands, remedy definitions. |
| `src/models/case.py` | Case lifecycle, claim payload, status transitions, and case metadata. |
| `src/models/ruling.py` | Structured ruling output: winner, confidence, reasoning, precedent refs (stubbed for M1), consequences. |
| `src/engine/canonicalize.py` | Normalize input data, dedupe evidence, validate hashes, standardize timestamps and enums. |
| `src/engine/evidence_score.py` | Assign a support score per evidence item using provenance, hash integrity, source trust, recency, and reliability. |
| `src/engine/predicate_eval.py` | Safely evaluate policy rule conditions with a whitelisted DSL only; no arbitrary Python execution. |
| `src/engine/policy_compiler.py` | Compile YAML policy templates into an internal AST / normalized rule set. |
| `src/engine/confidence.py` | Convert rule margin + evidence quality + counterevidence into `high/medium/low`. |
| `src/engine/ruling_engine.py` | End-to-end ruling orchestration: validate, score, evaluate rules, select outcome, generate reasoning. |
| `src/storage/sqlite_repo.py` | Persist cases, evidence, policies, and rulings on Railway with a simple durable store for M1. |
| `src/api/*.py` | Thin HTTP layer: request parsing, response serialization, auth hooks later. |
| `src/templates/*.yaml` | Human-editable policy templates for the first 3 dispute categories. |
| `tests/*` | Verify policy compilation, evidence scoring, confidence bands, and API contracts. |

### M1 design principle
Make the engine **deterministic first**, then optionally augment with an LLM-generated explanation. The actual ruling should be explainable from policy + evidence, not from free-form model output.

---

## 3) Ruling engine algorithm

M1 should use a **policy-first, evidence-weighted, rule-scored** pipeline.

### Inputs
- Case object
- Policy template selected by `policy_id` or template application
- Structured evidence items
- Optional case metadata: deadline, amount, dispute type, parties

### Step-by-step evaluation

1. **Validate and canonicalize**
   - Ensure required fields exist.
   - Canonicalize evidence timestamps to UTC.
   - Normalize hashes to a single format (`sha256:...`).
   - Reject malformed or duplicate evidence.

2. **Load policy template**
   - Resolve `policy_id` or `template_id` to a compiled policy.
   - Expand policy parameters into a normalized ruleset.
   - Enforce the correct dispute type (e.g. `delivery`, `milestone`, `quality`).

3. **Score each evidence item**
   - Compute `evidence_score` in `[0, 1]`.
   - Suggested weighting:
     - `source_trust` 30%
     - `hash_integrity` 25%
     - `reliability_score` 25%
     - `claimed_fact_specificity` 10%
     - `recency` 10%
   - Example formula:
     - `score = clamp(0, 1, 0.30*source_trust + 0.25*hash_integrity + 0.25*reliability_score + 0.10*specificity + 0.10*recency)`
   - If evidence hash cannot be verified, cap the score.

4. **Build fact graph**
   - Convert evidence into normalized facts such as:
     - delivered_before_deadline
     - work_matches_spec
     - bug_is_reproducible
     - bounty_disclosure_compliant
   - Associate each fact with supporting and opposing evidence IDs.

5. **Evaluate policy rules in priority order**
   - Each rule has:
     - `when` predicate
     - `then` outcome
     - `reason`
     - `confidence_hint`
     - optional `counterevidence` constraints
   - Evaluate rules against the fact graph.
   - Compute a **support score** and a **conflict score** for every matching rule.

6. **Select the ruling**
   - If a single rule dominates with a strong margin, issue a direct ruling.
   - If two rules are close, select `split` or `needs_more_info` depending on policy logic.
   - If no rule matches, fall back to the policy’s default clause.

7. **Assign confidence band**
   - `high` when:
     - strong rule match
     - clear evidence support
     - low conflict
   - `medium` when:
     - rule match exists but evidence is partially conflicting or incomplete
   - `low` when:
     - missing required evidence
     - conflicting evidence dominates
     - policy cannot resolve the case cleanly

8. **Generate ruling object**
   - Winner: `claimant`, `respondent`, or `split`
   - Reasoning: list of rule matches and evidence references
   - Consequences: non-custodial actions only in M1
     - reputation_update
     - payment_instruction
     - rework_required
     - release_requested
     - evidence_request
   - Include `appeal_deadline` only if you want it as a placeholder; appeals themselves are out of scope for M1.

### Example decision logic
- **Freelance delivery**:
  - If delivery proof hash verifies and timestamp is before deadline, favor respondent.
  - If no delivery proof exists and deadline passed, favor claimant.
  - If deliverable exists but quality evidence is below threshold, favor claimant or split with partial remedy.
- **Milestone payment**:
  - If milestone acceptance criteria are met, favor payee.
  - If criteria are partially met, allow partial release or rework.
- **Bug bounty**:
  - If reproducible exploit evidence meets severity threshold, favor researcher.
  - If disclosure rules were violated, downgrade or deny payout depending on template rules.

### Important constraint
No escrow logic should exist in M1. The engine can output a payment instruction or recommendation, but it should not hold or move money.

---

## 4) API endpoints needed for M1

Use a versioned API: `/v1/...`

### Required endpoints

#### Health
- `GET /health`
  - Liveness/readiness check for Railway.

#### Cases
- `POST /v1/cases`
  - Create a dispute case.
  - Stores claimant, respondent, policy_id, claim, and initial metadata.
- `GET /v1/cases`
  - List cases, with filters for `status`, `policy_id`, `party`, `limit`, `offset`.
- `GET /v1/cases/{case_id}`
  - Retrieve a case with stored evidence and ruling.

#### Evidence
- `POST /v1/cases/{case_id}/evidence`
  - Submit structured evidence.
  - Must accept the evidence-native fields:
    - `type`
    - `source`
    - `hash`
    - `claimed_fact`
    - `reliability_score`
- `GET /v1/cases/{case_id}/evidence`
  - Return all evidence items for a case.

#### Rulings
- `POST /v1/cases/{case_id}/ruling`
  - Trigger ruling generation.
- `GET /v1/cases/{case_id}/ruling`
  - Fetch the ruling if one exists.

#### Policies
- `POST /v1/policies`
  - Create a policy from a template or direct JSON payload.
- `GET /v1/policies`
  - List policies.
- `GET /v1/policies/{policy_id}`
  - Fetch a policy.

#### Templates
- `GET /v1/templates`
  - List built-in templates.
- `POST /v1/templates/{template_id}/apply`
  - Instantiate a policy from a template with parameters.

### Out of scope for M1
- Webhooks
- Precedent search
- Appeals
- Human fallback
- Escrow / custody / settlement routing

---

## 5) Policy template format

Use **YAML as the source format** for easy editing, and validate it against a JSON Schema at load time.

### Recommended YAML shape
```yaml
id: freelance-delivery:v1
name: Freelance Delivery Dispute Policy
version: 1.0.0
dispute_type: delivery
summary: Resolve client/freelancer disputes over delivery, quality, and payment.
parameters:
  deadline_grace_hours: 0
  minimum_quality_threshold: 0.8
  require_hash_verified_evidence: true
  source_trust_overrides:
    github: 0.9
    email: 0.6
    manual: 0.4
evidence_requirements:
  required_types: [contract, message, file]
  minimum_items: 2
  require_hash: true
  min_average_reliability: 0.6
rules:
  - id: delivered_on_time
    priority: 100
    when:
      all:
        - fact: delivery_proof_exists
          op: eq
          value: true
        - fact: delivery_timestamp
          op: lte_case_field
          field: deadline
    then:
      in_favor: respondent
      consequence:
        type: release_requested
        mode: external
      confidence_hint: high
    reason: Delivery proof exists and predates the deadline.
  - id: non_delivery
    priority: 90
    when:
      all:
        - fact: delivery_proof_exists
          op: eq
          value: false
        - fact: now
          op: gt_case_field
          field: deadline
    then:
      in_favor: claimant
      consequence:
        type: payment_instruction
        mode: external
      confidence_hint: high
    reason: No delivery proof was submitted before the deadline.
default_rule:
  in_favor: split
  consequence:
    type: evidence_request
    mode: advisory
  confidence_hint: low
  reason: Evidence is incomplete or contradictory.
```

### Shared JSON Schema requirements
At minimum, the policy template schema should require:
- `id`
- `name`
- `version`
- `dispute_type`
- `parameters`
- `evidence_requirements`
- `rules`
- `default_rule`

### Rule DSL constraints
To keep the engine safe and predictable, the condition language must be whitelisted:
- boolean operators: `all`, `any`, `not`
- comparisons: `eq`, `lt`, `lte`, `gt`, `gte`
- domain helpers: `exists`, `contains`, `hash_verified`, `source_is`, `reliability_gte`, `timestamp_before`, `timestamp_after`, `lte_case_field`

Do **not** allow arbitrary Python or expression evaluation.

### Starter templates to ship
1. `freelance-delivery`
   - Delivery timing, quality, and payment release disputes
2. `milestone-payment`
   - Milestone acceptance, partial completion, and payment release disputes
3. `bug-bounty`
   - Severity classification, reproducibility, and disclosure compliance disputes

---

## 6) Distribution strategy — how to get the first users

AgentCourt wins if it becomes the **default dispute layer for agent commerce**. The first users will not come from generic legal audiences; they will come from places already experiencing autonomous transaction friction.

### Primary wedge
Target users who already need a machine-readable dispute mechanism:
- AI agent builders
- freelance/contract workflows powered by agents
- bug bounty and security research workflows
- agent marketplaces and protocol teams
- Base / x402-native teams who want a lightweight dispute layer without escrow

### Why this wedge works
- No escrow lowers adoption friction and avoids custody complexity.
- Policy-first templates make AgentCourt easy to try without a long legal onboarding process.
- Structured evidence + confidence bands create trust and auditability.
- The output is API-native, so teams can plug it into their existing workflows.

### Distribution moves for first users
1. **Ship a public demo with the 3 templates**
   - One-click sample disputes.
   - Show the full ruling receipt: policy used, evidence table, confidence band, and reasoning.

2. **Open-source the core API and template format**
   - Developers adopt faster when they can inspect the rule engine.
   - Make templates easy to copy and customize.

3. **Partner with agent marketplaces and ecosystems**
   - List AgentCourt as the dispute layer for:
     - Virtuals / agent ecosystems
     - Agent marketplaces
     - Base-native commerce tools
   - Reach out to teams building agent-to-agent transactions.

4. **Use content + SEO around dispute templates**
   - Publish landing pages for:
     - freelance delivery dispute template
     - milestone payment dispute template
     - bug bounty dispute template
   - These are high-intent search terms.

5. **Create a viral sharing loop**
   - Every ruling should have a shareable receipt URL.
   - Include the template name, policy hash, and confidence band.
   - This makes the protocol visible every time a dispute is resolved.

6. **Direct outbound to design partners**
   - Start with 10–20 teams that already manage autonomous work or bounties.
   - Offer white-glove onboarding and template customization.

7. **Launch where builders hang out**
   - Product Hunt, X, Farcaster, GitHub, Base ecosystem communities, and agent forums.
   - Emphasize: “policy-driven dispute resolution for agents — no escrow.”

### Positioning message
> AgentCourt is the policy engine for agent disputes: submit evidence, apply a template, get a ruling — no escrow, no courtroom theater.

### First-90-day distribution priority
- Week 1: landing page + demo disputes + docs
- Week 2: open-source API + templates
- Week 3: 3–5 design partners
- Week 4: marketplace listings and ecosystem outreach
- Month 2: integration guides for agent frameworks and x402-native workflows
- Month 3: case studies and template marketplace

---

## Suggested M1 acceptance criteria
- FastAPI service deploys cleanly on Railway
- `/health` returns healthy
- Cases, evidence, policies, and rulings are persisted
- Rulings always include a confidence band
- Evidence input uses structured fields with hash and reliability score
- The engine resolves the three starter templates deterministically
- No escrow logic exists in the M1 code path

---

## Recommended next build step
Implement the template loader + deterministic ruling engine first, then wire the FastAPI routes around it.
