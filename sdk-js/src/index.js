/**
 * AgentCourt JavaScript SDK
 * Policy-driven dispute resolution for AI agent commerce.
 *
 * @module @agentcourt/sdk
 */

const DEFAULT_BASE_URL = "https://agentcourt-api-production.up.railway.app";

class AgentCourtError extends Error {
  constructor(message, statusCode) {
    super(message);
    this.name = "AgentCourtError";
    this.statusCode = statusCode;
  }
}

class PaymentRequiredError extends AgentCourtError {
  constructor(message, paymentChallenge) {
    super(message, 402);
    this.name = "PaymentRequiredError";
    this.paymentChallenge = paymentChallenge;
  }
}

class AgentCourt {
  /**
   * Create an AgentCourt client.
   * @param {Object} options
   * @param {string} [options.baseUrl] - AgentCourt API URL
   * @param {string} [options.apiKey] - Optional API key for paid tier
   */
  constructor(options = {}) {
    this.baseUrl = (options.baseUrl || DEFAULT_BASE_URL).replace(/\/$/, "");
    this.apiKey = options.apiKey || null;
  }

  async _request(method, path, data) {
    const url = `${this.baseUrl}${path}`;
    const headers = { "Content-Type": "application/json" };
    if (this.apiKey) headers["Authorization"] = `Bearer ${this.apiKey}`;

    const opts = { method, headers };
    if (data) opts.body = JSON.stringify(data);

    const resp = await fetch(url, opts);

    if (resp.status === 402) {
      const challenge = resp.headers.get("payment-required") || "";
      throw new PaymentRequiredError(
        "Payment required. You may have exceeded the free tier (100 disputes/month).",
        challenge
      );
    }

    if (!resp.ok) {
      const body = await resp.text();
      throw new AgentCourtError(`AgentCourt API error ${resp.status}: ${body}`, resp.status);
    }

    return resp.json();
  }

  /**
   * File a dispute and get a deterministic ruling.
   * @param {Object} params
   * @param {string} params.policy - Policy template name
   * @param {string} params.claim - What went wrong
   * @param {string} [params.desiredRemedy='full_refund'] - full_refund, partial_refund, or no_payout
   * @param {string} [params.claimant='agent'] - Who is filing
   * @param {string} [params.respondent='counterparty'] - Who is being disputed
   * @param {string[]} [params.contractObligations] - What was agreed
   * @param {Object} [params.metadata] - Structured facts
   * @param {Object[]} [params.evidence] - Supporting evidence
   * @returns {Promise<Object>} Ruling with ruling, confidence, case_id, reasoning
   */
  async fileDispute(params) {
    const {
      policy,
      claim,
      desiredRemedy = "full_refund",
      claimant = "agent",
      respondent = "counterparty",
      contractObligations = [],
      metadata = {},
      evidence = [],
    } = params;

    return this._request("POST", "/v1/disputes", {
      policy,
      claim,
      claimant,
      respondent,
      desired_remedy: desiredRemedy,
      contract: {
        parties: [claimant, respondent],
        obligations: contractObligations.length ? contractObligations : [claim],
      },
      metadata,
      evidence,
    });
  }

  /**
   * List all available policy templates.
   * @returns {Promise<Object[]>}
   */
  async listPolicies() {
    return this._request("GET", "/v1/policies");
  }

  /**
   * Get details for a specific policy.
   * @param {string} name - Policy name
   * @returns {Promise<Object>}
   */
  async getPolicy(name) {
    return this._request("GET", `/v1/policies/${name}`);
  }

  /**
   * Retrieve a filed case by ID.
   * @param {string} caseId
   * @returns {Promise<Object>}
   */
  async getCase(caseId) {
    return this._request("GET", `/v1/cases/${caseId}`);
  }

  /**
   * List recent cases.
   * @param {number} [limit=10]
   * @returns {Promise<Object[]>}
   */
  async listCases(limit = 10) {
    return this._request("GET", `/v1/cases?limit=${limit}`);
  }

  /**
   * Check API health.
   * @returns {Promise<Object>}
   */
  async health() {
    return this._request("GET", "/health");
  }
}

module.exports = { AgentCourt, AgentCourtError, PaymentRequiredError };
