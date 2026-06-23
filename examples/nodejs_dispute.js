/**
 * Node.js Example: AgentCourt Dispute Resolution
 * 
 * npm install
 * (uses built-in fetch in Node 18+)
 */

const AGENTCOURT_BASE = 'https://agentcourt-api-production.up.railway.app';

async function fileDispute(dispute) {
  const response = await fetch(`${AGENTCOURT_BASE}/v1/disputes`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      policy: dispute.policy,
      claim: dispute.claim,
      claimant: dispute.claimant || 'node-agent',
      respondent: dispute.respondent || 'api-service',
      desired_remedy: dispute.remedy || 'full_refund',
      contract: {
        parties: [dispute.claimant || 'node-agent', dispute.respondent || 'api-service'],
        obligations: [dispute.obligation || 'Provide correct service']
      },
      metadata: {
        response_received: true,
        schema_matches: dispute.schemaMatches ?? false,
        ...dispute.metadata
      },
      evidence: dispute.evidence || [{
        type: 'log',
        source: 'node-agent',
        timestamp: new Date().toISOString(),
        claimed_fact: dispute.claim
      }]
    })
  });
  return response.json();
}

// Example: API returned wrong format
async function main() {
  const ruling = await fileDispute({
    policy: 'api-quality',
    claim: 'API returned XML instead of JSON',
    obligation: 'Return JSON response',
    schemaMatches: false,
    remedy: 'full_refund',
    evidence: [{
      type: 'http-response',
      source: 'fetch',
      timestamp: new Date().toISOString(),
      claimed_fact: 'Content-Type: text/xml (expected application/json)'
    }]
  });

  console.log('Ruling:', ruling.ruling);
  console.log('Confidence:', `${(ruling.confidence * 100).toFixed(0)}%`);
  console.log('Case ID:', ruling.case_id);
  console.log('Reasoning:', ruling.reasoning);
}

main().catch(console.error);
