# AgentCourt Launch Thread — @vbkotecha

## Thread: "Agent commerce needs a court, not escrow"

1/ AI agents are starting to transact. They're buying APIs, hiring other agents, delivering work, and moving money.

But there's a missing layer nobody's talking about:

What happens when the agent is wrong?

2/ Today, the answer is: nothing.

No dispute resolution. No accountability. No recourse.

The buyer eats the cost. The marketplace absorbs the risk. The trust tax gets passed to everyone.

3/ Escrow doesn't fix this. Escrow just holds money hostage.

The real question isn't "who has the money?" — it's "who's right?"

That's a policy question, not a custody question.

4/ That's why we built AgentCourt.

AgentCourt is a policy-driven dispute resolution layer for agent commerce.

You submit evidence. You apply policy rules. You get a ruling.

5/ No courtroom theater. No escrow. No smart contract custody.

Just:
- Evidence (contracts, commits, logs, hashes)
- Policy (rules you define or use from templates)
- Ruling (with confidence band, remedy, and audit trail)

6/ Here's what a ruling looks like:

```
Policy: freelance-delivery
Rule: non-delivery
Confidence: HIGH
Remedy: full_refund
```

"The respondent failed to deliver the agreed-upon work. No deliverable was produced or submitted."

7/ Every ruling includes:
- Confidence band (high/medium/low)
- Evidence scoring (weighted by type, reliability, recency)
- Facts established vs facts unknown
- Full audit trail

You can see exactly WHY the ruling was made.

8/ We're shipping with 3 policy templates:
- Freelance delivery disputes (non-delivery, late delivery, scope creep)
- Milestone payment disputes (unpaid milestones, overdue payments)
- Bug bounty disputes (reproducibility, severity, disclosure compliance)

Each template has 5 rules with conditions, confidence bands, and remedies.

9/ The API is live right now:

```
POST https://agentcourt-api-production.up.railway.app/v1/disputes
GET /v1/policies
GET /docs
```

It's deterministic. The same evidence + policy always produces the same ruling.

10/ Our thesis:

Agent commerce will be bigger than e-commerce. But it won't happen without trust infrastructure.

Escrow is the wrong primitive. Policy-based rulings are the right one.

11/ We're looking for 5 design partners.

If you're building:
- Agent marketplaces
- x402 payment flows
- Freelance platforms
- AI service marketplaces

DM me. We'll map your disputes to structured rulings.

12/ AgentCourt is live. Policies are open. API is public.

No escrow. No courtroom. Just evidence, policy, and rulings.

The dispute layer for agent commerce.

🔗 agentcourt-api-production.up.railway.app/docs
