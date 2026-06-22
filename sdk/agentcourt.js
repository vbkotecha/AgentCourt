/**
 * AgentCourt JavaScript SDK
 * =========================
 * npm install agentcourt  (coming soon)
 * or copy this file into your project.
 *
 * Usage:
 *   import { AgentCourt } from './agentcourt.js';
 *
 *   const court = new AgentCourt();
 *
 *   const ruling = await court.resolve({
 *     policy: 'freelance-delivery',
 *     claim: 'Work never delivered',
 *     claimant: 'buyer_agent',
 *     respondent: 'freelancer_bot',
 *     desiredRemedy: 'full_refund',
 *     evidence: [...]
 *   });
 *
 *   console.log(ruling.remedy);      // 'full_refund'
 *   console.log(ruling.confidence);  // 'high'
 */

const DEFAULT_API = 'https://agentcourt-api-production.up.railway.app';

export class AgentCourt {
  /**
   * Create an AgentCourt client.
   * @param {string} apiUrl - API base URL
   * @param {number} timeout - Request timeout in ms
   */
  constructor(apiUrl = DEFAULT_API, timeout = 30000) {
    this.apiUrl = apiUrl.replace(/\/$/, '');
    this.timeout = timeout;
  }

  async _post(path, data) {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), this.timeout);
    try {
      const res = await fetch(`${this.apiUrl}${path}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
        signal: controller.signal,
      });
      if (!res.ok) {
        const text = await res.text();
        throw new Error(`HTTP ${res.status}: ${text}`);
      }
      return await res.json();
    } finally {
      clearTimeout(timer);
    }
  }

  async _get(path) {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), this.timeout);
    try {
      const res = await fetch(`${this.apiUrl}${path}`, {
        signal: controller.signal,
      });
      if (!res.ok) {
        throw new Error(`HTTP ${res.status}`);
      }
      return await res.json();
    } finally {
      clearTimeout(timer);
    }
  }

  /**
   * Submit a dispute and get a ruling.
   * @param {Object} params
   * @param {string} params.policy - Policy template name
   * @param {string} params.claim - Description of the dispute
   * @param {string} params.claimant - Party filing the claim
   * @param {string} params.respondent - Party being claimed against
   * @param {string} [params.desiredRemedy='full_refund'] - What claimant wants
   * @param {Array} [params.evidence=[]] - Evidence items
   * @param {Object} [params.metadata={}] - Structured facts
   * @param {Object} [params.contract={}] - Contract details
   * @returns {Promise<Object>} Ruling object
   *
   * @example
   * const ruling = await court.resolve({
   *   policy: 'sla-monitoring',
   *   claim: 'SLA violation',
   *   claimant: 'client',
   *   respondent: 'provider',
   *   metadata: {
   *     required_uptime: 99.9,
   *     actual_uptime: 98.5,
   *     monitoring_period_confirmed: true
   *   },
   *   evidence: [
   *     { type: 'contract', source: 'sla.pdf',
   *       timestamp: '2026-06-01',
   *       claimed_fact: 'SLA requires 99.9 percent uptime' }
   *   ]
   * });
   */
  async resolve(params) {
    const payload = {
      policy: params.policy,
      claim: params.claim,
      claimant: params.claimant,
      respondent: params.respondent,
      desired_remedy: params.desiredRemedy || 'full_refund',
      evidence: params.evidence || [],
    };
    if (params.metadata) payload.metadata = params.metadata;
    if (params.contract) payload.contract = params.contract;

    const raw = await this._post('/v1/disputes', payload);

    return {
      caseId: raw.case_id || '',
      status: raw.status || '',
      matchedRule: raw.matched_rule_id || '',
      remedy: raw.remedy || '',
      confidence: raw.confidence || '',
      rulingText: raw.ruling || '',
      reasoning: raw.reasoning || '',
      policyName: raw.policy_name || '',
      evidenceScores: raw.evidence_scores || [],
      factsEstablished: raw.facts_established || [],
      factsDisputed: raw.facts_disputed || [],
      factsUnknown: raw.facts_unknown || [],
      ruledAt: raw.ruled_at || '',
      engineVersion: raw.engine_version || '',
      raw,
    };
  }

  /** List all available policy templates. */
  async listPolicies() {
    return await this._get('/v1/policies');
  }

  /** Get details of a specific policy template. */
  async getPolicy(name) {
    return await this._get(`/v1/policies/${name}`);
  }

  /** Look up a previous verdict by case ID. */
  async getVerdict(caseId) {
    return await this._get(`/v1/cases/${caseId}`);
  }

  /** List all stored verdicts. */
  async listVerdicts() {
    return await this._get('/v1/verdicts');
  }

  /** Check API health. */
  async health() {
    return await this._get('/health');
  }
}

/**
 * Convenience function: resolve a dispute in one call.
 * @example
 * import { resolveDispute } from './agentcourt.js';
 * const ruling = await resolveDispute({
 *   policy: 'freelance-delivery',
 *   claim: 'Work never delivered',
 *   claimant: 'buyer',
 *   respondent: 'seller',
 *   evidence: [...]
 * });
 */
export async function resolveDispute(params) {
  return new AgentCourt().resolve(params);
}

// ─── CommonJS fallback (for Node require) ────────────────────────────────
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { AgentCourt, resolveDispute };
}

// ─── Example ──────────────────────────────────────────────────────────────

// Uncomment to test:
/*
async function main() {
  const court = new AgentCourt();
  const health = await court.health();
  console.log(`API: ${health.status} | ${health.policies.length} policies`);

  const ruling = await court.resolve({
    policy: 'physical-commerce',
    claim: 'Wrong product delivered',
    claimant: 'shopping_agent',
    respondent: 'merchant_store',
    desiredRemedy: 'full_refund',
    contract: {
      parties: ['shopping_agent', 'merchant_store'],
      obligations: ['Deliver correct product'],
      deadlines: ['2026-06-25'],
    },
    metadata: {
      delivery_confirmed: true,
      received_matches_order: false,
      ordered_product: 'Blue sneakers size 10',
      received_product: 'Red sneakers size 10',
    },
    evidence: [
      { type: 'contract', source: 'order', timestamp: '2026-06-20',
        claimed_fact: 'Ordered blue sneakers' },
      { type: 'log', source: 'photo', timestamp: '2026-06-22',
        claimed_fact: 'Received red sneakers' },
    ],
  });
  console.log(`Remedy: ${ruling.remedy} (${ruling.confidence})`);
}
main().catch(console.error);
*/
