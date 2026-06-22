# Contributing to AgentCourt

Thank you for your interest in contributing to AgentCourt! This document outlines the process for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/agentcourt/agentcourt.git`
3. Install dependencies: `pip install -r requirements.txt`
4. Run the test suite: `python -m pytest tests/`

## Development Setup

```bash
# Run the API locally
cd src/
python -u main.py

# Run tests
python tests/test_policy_engine.py

# Verify all policies load
curl http://localhost:8000/v1/policies
```

## Adding a New Policy Template

Policy templates are JSON files in `src/policies/`. Each template defines:

1. **Evidence weights** — override defaults for specific evidence types
2. **Fact extraction rules** — patterns to detect in evidence text
3. **Rules** — boolean conditions over extracted facts
4. **Confidence bands** — when to assign high/medium/low confidence

### Example

```json
{
  "name": "my-policy",
  "version": "1.0.0",
  "evidence_weights": { ... },
  "extraction_rules": { ... },
  "rules": [
    {
      "id": "rule-1",
      "condition": "fact_a == true AND fact_b == false",
      "confidence": "medium",
      "remedy": "full_refund",
      "ruling_template": "Rule 1 matched because ..."
    }
  ]
}
```

### Testing Your Policy

Add test cases to `tests/test_policy_engine.py`:

```python
def test_my_policy_scenario():
    result = evaluate_dispute(
        policy="my-policy",
        contract={...},
        evidence=[...]
    )
    assert result["matched_rule_id"] == "rule-1"
    assert result["remedy"] == "full_refund"
```

## Pull Request Process

1. Create a feature branch: `git checkout -b feature/my-new-policy`
2. Write tests for your changes
3. Ensure all tests pass: `python tests/test_policy_engine.py`
4. Commit with clear messages
5. Open a PR describing what changed and why

## Code Style

- Python: PEP 8
- JSON: 2-space indentation
- Policy names: kebab-case (e.g., `freelance-delivery`)
- Rule IDs: kebab-case (e.g., `non-delivery`)

## Reporting Issues

Use GitHub Issues. Include:
- Policy name and version
- Dispute input (anonymized)
- Expected vs actual ruling
- Steps to reproduce

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
