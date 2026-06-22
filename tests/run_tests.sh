#!/bin/bash
# AgentCourt API — Test Runner
# =============================
# Runs the full test suite against the LIVE API and outputs a clean summary.
#
# Usage: bash /root/.letta/agentcourt/tests/run_tests.sh

set -e

echo "═══════════════════════════════════════════════════════════"
echo "  AgentCourt API — Comprehensive Test Suite"
echo "  Target: https://agentcourt-api-production.up.railway.app"
echo "═══════════════════════════════════════════════════════════"
echo ""

# Check if pytest is installed
if ! command -v pytest &> /dev/null; then
    echo "❌ pytest not found. Installing..."
    pip install pytest requests -q
fi

# Check API health first
echo "Checking API health..."
HEALTH=$(curl -s -o /dev/null -w "%{http_code}" https://agentcourt-api-production.up.railway.app/health --max-time 10)
if [ "$HEALTH" != "200" ]; then
    echo "❌ API is not responding (HTTP $HEALTH). Aborting tests."
    exit 1
fi
echo "✅ API is healthy"
echo ""

# Run tests
python3 -m pytest /root/.letta/agentcourt/tests/test_suite.py -v \
    --tb=short \
    --strict-markers \
    -rA \
    2>&1 | tee /tmp/agentcourt_test_output.txt

# Extract summary
echo ""
echo "═══════════════════════════════════════════════════════════"
echo "  SUMMARY"
echo "═══════════════════════════════════════════════════════════"

PASSED=$(grep -c "PASSED" /tmp/agentcourt_test_output.txt || echo "0")
FAILED=$(grep -c "FAILED" /tmp/agentcourt_test_output.txt || echo "0")
ERRORS=$(grep -c "ERROR" /tmp/agentcourt_test_output.txt || echo "0")
TOTAL=$((PASSED + FAILED + ERRORS))

echo "  Total Tests:  $TOTAL"
echo "  ✅ Passed:     $PASSED"
echo "  ❌ Failed:     $FAILED"
echo "  ⚠️  Errors:    $ERRORS"
echo ""

if [ "$FAILED" -eq 0 ] && [ "$ERRORS" -eq 0 ]; then
    echo "  🏆 ALL TESTS PASSED"
    exit 0
else
    echo "  💀 SOME TESTS FAILED — see details above"
    exit 1
fi
