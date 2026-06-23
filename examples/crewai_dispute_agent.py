"""
CrewAI Integration: Dispute Resolution Agent

Add AgentCourt as a capability to your CrewAI crew.
When agents detect a problem with a transaction, they can file a dispute.

pip install crewai requests
"""
import requests
from crewai.tools import tool

AGENTCOURT_BASE = "https://agentcourt-api-production.up.railway.app"


@tool("File Dispute")
def file_dispute(policy: str, claim: str, meets_spec: bool, evidence: str) -> str:
    """File a dispute with AgentCourt's policy-driven resolution engine.
    
    Args:
        policy: The dispute policy to apply (api-quality, freelance-delivery, 
                milestone-payment, bug-bounty, sla-monitoring, scope-dispute, physical-commerce)
        claim: What went wrong in the transaction
        meets_spec: Whether the deliverable met agreed specifications
        evidence: Factual description of evidence
    
    Returns:
        Human-readable ruling summary
    """
    response = requests.post(f"{AGENTCOURT_BASE}/v1/disputes", json={
        "policy": policy,
        "claim": claim,
        "claimant": "crew-agent",
        "respondent": "counterparty",
        "desired_remedy": "full_refund",
        "contract": {"parties": ["crew-agent", "counterparty"], "obligations": [claim]},
        "metadata": {"delivered": True, "meets_spec": meets_spec},
        "evidence": [{"type": "observation", "source": "crew", "claimed_fact": evidence}]
    })
    ruling = response.json()
    return f"Ruling: {ruling['ruling']} | Confidence: {ruling['confidence']:.0%} | Case: {ruling['case_id']}"


# Usage in a CrewAI crew
if __name__ == "__main__":
    from crewai import Agent, Task, Crew
    
    dispute_agent = Agent(
        role="Dispute Resolution Specialist",
        goal="File and resolve disputes when agent transactions go wrong",
        backstory="An AI agent specialized in evaluating transaction quality and filing disputes.",
        tools=[file_dispute],
        verbose=True
    )
    
    # Example task
    resolve_task = Task(
        description="An API we paid for returned malformed data. File a dispute.",
        agent=dispute_agent,
        expected_output="A dispute ruling from AgentCourt"
    )
    
    crew = Crew(agents=[dispute_agent], tasks=[resolve_task])
    # result = crew.kickoff()
    print("CrewAI dispute agent ready. Uncomment crew.kickoff() to run.")
