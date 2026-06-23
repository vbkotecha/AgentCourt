# Glama.ai MCP Server Submission

## Steps for Vivek

1. Go to: https://glama.ai/mcp/servers/submit
2. Fill in:

**Server Name:** AgentCourt

**Description:**
Policy-driven dispute resolution MCP server for AI agent commerce. When agents transact and things go wrong (API schema mismatch, non-delivery, SLA breach), this MCP server lets your AI assistant file disputes and get deterministic rulings in under 500ms.

**Server URL/Command:**
```
python3 https://raw.githubusercontent.com/vbkotecha/agentcourt-api/main/mcp-server/server.py
```

**Category:** Legal / Infrastructure

**Tags:** dispute-resolution, agent-commerce, x402, base, trust, verification

**GitHub:** https://github.com/vbkotecha/agentcourt-api

**Tools (6):**
1. `file_dispute` — File a dispute and get a ruling
2. `list_policies` — List available policy templates
3. `get_policy_details` — Get details of a specific policy
4. `get_case` — Get case details by ID
5. `list_verdicts` — List recent verdicts
6. `health_check` — Check API health

3. Submit
4. Wait for approval
5. Comment on PR https://github.com/punkpeye/awesome-mcp-servers/pull/8570 with the Glama URL

This unblocks the 89K★ awesome-mcp-servers listing!
