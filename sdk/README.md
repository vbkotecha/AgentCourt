# AgentCourt SDK

Zero-dependency SDKs for the AgentCourt dispute resolution API.

## Installation

### Python
```bash
pip install agentcourt
```

### JavaScript / TypeScript
```bash
npm install @agentcourt/sdk
```

## Quick Start

### Python
```python
from agentcourt_python_sdk import AgentCourt
court = AgentCourt()
ruling = court.dispute(
    policy="api-quality",
    claim="Schema mismatch",
    desired_remedy="full_refund",
    evidence=[{"type": "log", "source": "resp.json", "claimed_fact": "Wrong type"}],
)
print(ruling.remedy)  # full_refund
```

### JavaScript
```javascript
const court = new AgentCourt();
const ruling = await court.resolve({
    policy: 'api-quality',
    claim: 'Schema mismatch',
    desiredRemedy: 'full_refund',
    evidence: [{type: 'log', source: 'resp.json', claimedFact: 'Wrong type'}],
});
console.log(ruling.remedy); // full_refund
```

## License

MIT
