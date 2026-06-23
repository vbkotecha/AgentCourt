/**
 * AgentCourt TypeScript definitions
 */

export interface Ruling {
  ruling: "full_refund" | "partial_refund" | "no_payout" | string;
  confidence: number;
  case_id: string;
  reasoning: string;
  policy: string;
  [key: string]: any;
}

export interface Policy {
  name: string;
  description: string;
  version: string;
  rule_count: number;
  rules?: Rule[];
}

export interface Rule {
  id: string;
  condition: string;
  ruling: string;
  confidence: number;
  reasoning: string;
}

export interface DisputeParams {
  policy: string;
  claim: string;
  desiredRemedy?: "full_refund" | "partial_refund" | "no_payout";
  claimant?: string;
  respondent?: string;
  contractObligations?: string[];
  metadata?: Record<string, any>;
  evidence?: Array<Record<string, any>>;
}

export interface AgentCourtOptions {
  baseUrl?: string;
  apiKey?: string;
}

export class AgentCourtError extends Error {
  statusCode: number;
}

export class PaymentRequiredError extends AgentCourtError {
  paymentChallenge: string;
}

export class AgentCourt {
  constructor(options?: AgentCourtOptions);
  fileDispute(params: DisputeParams): Promise<Ruling>;
  listPolicies(): Promise<Policy[]>;
  getPolicy(name: string): Promise<Policy>;
  getCase(caseId: string): Promise<any>;
  listCases(limit?: number): Promise<any[]>;
  health(): Promise<any>;
}
