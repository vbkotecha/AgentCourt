"""
LangChain Tool: AgentCourt Dispute Resolution

Add this tool to any LangChain agent to give it the ability to
file disputes when transactions go wrong.

pip install langchain requests
"""
from langchain.tools import tool
import requests
from typing import Optional

AGENTCOURT_BASE = "https://agentcourt-api-production.up.railway.app"


@tool
def file_dispute(
    policy: str,
    claim: str,
    claimant: str,
    respondent: str,
    desired_remedy: str,
    delivered: bool,
    meets_spec: bool,
    evidence_description: str,
) -> dict:
    """
    File a dispute with AgentCourt when an agent commerce transaction goes wrong.
    
    Args:
        policy: One of: api-quality, freelance-delivery, milestone-payment,
                bug-bounty, sla-monitoring, scope-dispute, physical-commerce
        claim: Description of what went wrong
        claimant: The party filing the dispute
        respondent: The party being disputed against
        desired_remedy: full_refund, partial_refund, or no_payout
        delivered: Whether the deliverable was received
        meets_spec: Whether the deliverable met the agreed specification
        evidence_description: Factual description of the evidence
    
    Returns:
        Ruling dict with: ruling, confidence, case_id, reasoning
    """
    response = requests.post(f"{AGENTCOURT_BASE}/v1/disputes", json={
        "policy": policy,
        "claim": claim,
        "claimant": claimant,
        "respondent": respondent,
        "desired_remedy": desired_remedy,
        "contract": {
            "parties": [claimant, respondent],
            "obligations": [claim]
        },
        "metadata": {
            "delivered": delivered,
            "meets_spec": meets_spec,
            "response_received": delivered
        },
        "evidence": [{
            "type": "log",
            "source": "agent-observation",
            "timestamp": "2026-06-23T00:00:00Z",
            "claimed_fact": evidence_description
        }]
    })
    return response.json()


# Usage with LangChain agent
if __name__ == "__main__":
    from langchain.agents import AgentExecutor, create_openai_tools_agent
    from langchain_openai import ChatOpenAI
    from langchain_core.prompts import ChatPromptTemplate
    
    # Add dispute resolution to any agent
    tools = [file_dispute]
    
    # Example: Agent detects bad API response and files dispute
    result = file_dispute.invoke({
        "policy": "api-quality",
        "claim": "API returned XML instead of JSON",
        "claimant": "my-agent",
        "respondent": "data-api",
        "desired_remedy": "full_refund",
        "delivered": True,
        "meets_spec": False,
        "evidence_description": "Response Content-Type was text/xml, expected application/json"
    })
    print(f"Ruling: {result['ruling']} (confidence: {result['confidence']})")
    print(f"Case ID: {result['case_id']}")
