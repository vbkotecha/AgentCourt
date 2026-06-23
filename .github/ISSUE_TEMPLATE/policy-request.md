---
name: Policy Request
about: Request a new dispute resolution policy template
title: "[Policy] "
labels: policy-request
assignees: ''
---

## Policy Name
<!-- e.g., "data-privacy-breach", "nft-authenticity", "subscription-cancellation" -->

## Use Case
<!-- Describe the scenario this policy would cover -->

## Evidence Structure
<!-- What metadata fields would the policy evaluate? -->

```json
{
  "metadata": {
    "field1": "",
    "field2": false
  }
}
```

## Expected Rules
<!-- List the conditions and rulings -->

| Condition | Ruling | Confidence | Reasoning |
|-----------|--------|------------|-----------|
| metadata.field == false | full_refund | 0.95 | Description |
| metadata.field == true | claim_denied | 0.90 | Description |

## Real-World Example
<!-- Describe a real dispute this policy would resolve -->
