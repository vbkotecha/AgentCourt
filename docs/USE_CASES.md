# AgentCourt Use Cases

Real-world scenarios where AgentCourt resolves disputes between autonomous agents.

## 1. API Marketplace Quality Dispute

**Scenario:** An AI agent pays $0.02 via x402 to call a weather API. The response is XML instead of JSON.

**Policy:** `api-quality` → Rule: `schema-mismatch`

```json
{
  "policy": "api-quality",
  "claim": "API returned XML instead of declared JSON schema",
  "desired_remedy": "full_refund",
  "metadata": {
    "response_received": true,
    "schema_matches": false,
    "mismatched_field": "root_element",
    "expected_type": "JSON object",
    "actual_type": "XML document"
  }
}
```

**Ruling:** Full refund. Confidence: high. < 500ms.

---

## 2. Freelance Agent Non-Delivery

**Scenario:** A coding agent was hired to deliver a Python module by Friday. It's Monday. No delivery.

**Policy:** `freelance-delivery` → Rule: `deadline-passed-no-delivery`

```json
{
  "policy": "freelance-delivery",
  "claim": "Agent failed to deliver Python module by deadline",
  "desired_remedy": "full_refund",
  "metadata": {
    "delivered": false,
    "deadline_passed": true,
    "payment_made": true,
    "deadline_date": "2026-06-20"
  }
}
```

**Ruling:** Full refund. Confidence: high.

---

## 3. SLA Monitoring Violation

**Scenario:** An AI infra agent guarantees 99.9% uptime. Actual uptime was 97.5%.

**Policy:** `sla-monitoring` → Rule: `uptime-below-threshold`

```json
{
  "policy": "sla-monitoring",
  "claim": "Uptime below contracted 99.9% SLA",
  "desired_remedy": "partial_refund",
  "metadata": {
    "uptime_percentage": 97.5,
    "sla_threshold": 99.9,
    "measurement_period": "30 days",
    "incidents": 4
  }
}
```

**Ruling:** Partial refund (SLA credits). Confidence: high.

---

## 4. Bug Bounty Severity Dispute

**Scenario:** A security agent found a reproducible vulnerability. The bounty platform classified it as "low" severity. The agent argues it's "critical."

**Policy:** `bug-bounty` → Rule: `severity-mismatch`

```json
{
  "policy": "bug-bounty",
  "claim": "Critical bug rejected as low severity",
  "desired_remedy": "full_payout",
  "metadata": {
    "is_reproducible": true,
    "severity": "critical",
    "severity_threshold": "high",
    "cvss_score": 9.8
  }
}
```

**Ruling:** Full payout at critical rate. Confidence: high.

---

## 5. Milestone Payment Dispute

**Scenario:** An agent completed Milestone 2 of a 5-milestone contract. The payer refuses to release payment.

**Policy:** `milestone-payment` → Rule: `milestone-completed-unpaid`

```json
{
  "policy": "milestone-payment",
  "claim": "Milestone 2 completed but payment withheld",
  "desired_remedy": "release_funds",
  "metadata": {
    "milestone_completed": true,
    "milestone_approved": true,
    "payment_released": false,
    "milestone_amount": "$500"
  }
}
```

**Ruling:** Release milestone payment. Confidence: high.

---

## 6. Scope Creep in Agent Contract

**Scenario:** A data processing agent was hired for 10 hours of work. The client keeps adding requirements. The agent is now at 25 hours.

**Policy:** `scope-dispute` → Rule: `scope-exceeded`

```json
{
  "policy": "scope-dispute",
  "claim": "Scope exceeded original 10-hour estimate by 150%",
  "desired_remedy": "renegotiate",
  "metadata": {
    "estimated_hours": 10,
    "actual_hours": 25,
    "exceeds_threshold": true,
    "original_scope": "data cleaning",
    "actual_scope": "data cleaning + ML model + deployment"
  }
}
```

**Ruling:** Renegotiate contract terms. Confidence: medium.

---

## 7. Physical Commerce Damage

**Scenario:** An autonomous drone delivery agent delivered a package. The contents were damaged.

**Policy:** `physical-commerce` → Rule: `damaged-on-arrival`

```json
{
  "policy": "physical-commerce",
  "claim": "Package contents damaged during delivery",
  "desired_remedy": "replace",
  "metadata": {
    "item_received": true,
    "item_damaged": true,
    "packaging_intact": false,
    "item_value": "$1,200"
  }
}
```

**Ruling:** Replace item. Confidence: high.

---

## Integration Patterns

### Pattern 1: Marketplace Embed
```
Buyer Agent → Marketplace → Seller Agent
                    ↓
              AgentCourt (if dispute)
```

### Pattern 2: Direct Agent-to-Agent
```
Agent A ←→ Agent B
    ↓ (dispute)
AgentCourt API
```

### Pattern 3: MCP-Powered
```
Claude/Cursor → MCP Server → AgentCourt
```

### Pattern 4: CI/CD Pipeline
```
GitHub Action → AgentCourt (automated SLA check)
```

### Pattern 5: ElizaOS Agent
```
ElizaOS Agent → FILE_DISPUTE action → AgentCourt
```
