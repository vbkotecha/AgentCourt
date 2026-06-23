/**
 * AgentCourt Plugin for ElizaOS
 *
 * Provides dispute resolution actions for ElizaOS agents.
 * Agents can file disputes when agent commerce transactions go wrong.
 */

export interface AgentCourtConfig {
  baseUrl?: string;
  apiKey?: string;
}

export interface DisputeParams {
  policy: string;
  claim: string;
  desiredRemedy?: string;
  claimant?: string;
  respondent?: string;
  metadata?: Record<string, any>;
  evidence?: Array<Record<string, any>>;
}

const DEFAULT_BASE_URL = "https://agentcourt-api-production.up.railway.app";

/**
 * File a dispute with AgentCourt and get a deterministic ruling.
 */
export async function fileDispute(
  params: DisputeParams,
  config: AgentCourtConfig = {}
): Promise<any> {
  const baseUrl = (config.baseUrl || DEFAULT_BASE_URL).replace(/\/$/, "");
  const {
    policy,
    claim,
    desiredRemedy = "full_refund",
    claimant = "eliza-agent",
    respondent = "counterparty",
    metadata = {},
    evidence = [],
  } = params;

  const response = await fetch(`${baseUrl}/v1/disputes`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      policy,
      claim,
      claimant,
      respondent,
      desired_remedy: desiredRemedy,
      contract: {
        parties: [claimant, respondent],
        obligations: [claim],
      },
      metadata,
      evidence,
    }),
  });

  if (response.status === 402) {
    throw new Error(
      "Payment required. Free tier limit (100/month) exceeded. Include x402 payment for paid disputes."
    );
  }

  if (!response.ok) {
    throw new Error(`AgentCourt API error: ${response.status}`);
  }

  return response.json();
}

/**
 * List available dispute resolution policies.
 */
export async function listPolicies(config: AgentCourtConfig = {}): Promise<any> {
  const baseUrl = (config.baseUrl || DEFAULT_BASE_URL).replace(/\/$/, "");
  const response = await fetch(`${baseUrl}/v1/policies`);
  if (!response.ok) throw new Error(`AgentCourt API error: ${response.status}`);
  return response.json();
}

/**
 * Check AgentCourt API health.
 */
export async function healthCheck(config: AgentCourtConfig = {}): Promise<any> {
  const baseUrl = (config.baseUrl || DEFAULT_BASE_URL).replace(/\/$/, "");
  const response = await fetch(`${baseUrl}/health`);
  if (!response.ok) throw new Error(`AgentCourt API error: ${response.status}`);
  return response.json();
}

// ElizaOS plugin export
export const AgentCourtPlugin = {
  name: "agentcourt",
  description: "Dispute resolution for agent commerce",
  actions: [
    {
      name: "FILE_DISPUTE",
      description: "File a dispute when an agent commerce transaction goes wrong",
      handler: async (runtime: any, message: any, state: any) => {
        const config: AgentCourtConfig = {
          baseUrl: runtime.getSetting("AGENTCOURT_BASE_URL") || DEFAULT_BASE_URL,
          apiKey: runtime.getSetting("AGENTCOURT_API_KEY"),
        };
        // Parse dispute details from message
        const result = await fileDispute(
          {
            policy: state?.policy || "api-quality",
            claim: state?.claim || message.content,
            desiredRemedy: state?.desiredRemedy || "full_refund",
            metadata: state?.metadata || {},
          },
          config
        );
        return result;
      },
    },
    {
      name: "CHECK_POLICIES",
      description: "List available dispute resolution policies",
      handler: async (runtime: any) => {
        const config: AgentCourtConfig = {
          baseUrl: runtime.getSetting("AGENTCOURT_BASE_URL") || DEFAULT_BASE_URL,
        };
        return listPolicies(config);
      },
    },
  ],
};

export default AgentCourtPlugin;
