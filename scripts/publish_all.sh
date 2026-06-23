#!/bin/bash
# AgentCourt One-Shot Publisher
# Run this after setting up npm and PyPI tokens
# Usage: NPM_TOKEN=xxx PYPI_TOKEN=xxx bash scripts/publish_all.sh

set -e

echo "🚀 AgentCourt Publisher — Publishing all packages"
echo "================================================"

# --- NPM Packages ---
if [ -z "$NPM_TOKEN" ]; then
    echo "⚠️  NPM_TOKEN not set — skipping npm packages"
else
    echo "npm config set //registry.npmjs.org/:_authToken \$NPM_TOKEN"
    npm config set //registry.npmjs.org/:_authToken "$NPM_TOKEN"

    # 1. JS SDK
    echo ""
    echo "📦 Publishing @agentcourt/sdk..."
    cd /root/.letta/agentcourt/sdk-js
    npm publish --access public
    echo "✅ @agentcourt/sdk published"

    # 2. MCP Server
    echo ""
    echo "📦 Publishing @agentcourt/mcp-server..."
    cd /root/.letta/agentcourt/mcp-server
    npm publish --access public
    echo "✅ @agentcourt/mcp-server published"

    # 3. ElizaOS Plugin
    echo ""
    echo "📦 Publishing @agentcourt/elizaos-plugin..."
    cd /root/.letta/agentcourt/elizaos-plugin
    npm publish --access public
    echo "✅ @agentcourt/elizaos-plugin published"
fi

# --- PyPI Package ---
if [ -z "$PYPI_TOKEN" ]; then
    echo ""
    echo "⚠️  PYPI_TOKEN not set — skipping Python package"
else
    echo ""
    echo "📦 Publishing agentcourt to PyPI..."
    cd /root/.letta/agentcourt/sdk-python
    python3 setup.py sdist bdist_wheel
    TWINE_PASSWORD="$PYPI_TOKEN" TWINE_USERNAME="__token__" twine upload dist/*
    echo "✅ agentcourt published to PyPI"
fi

echo ""
echo "================================================"
echo "✅ All packages published!"
echo ""
echo "Verify:"
echo "  npm view @agentcourt/sdk"
echo "  npm view @agentcourt/mcp-server"
echo "  npm view @agentcourt/elizaos-plugin"
echo "  pip install agentcourt"
