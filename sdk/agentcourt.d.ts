/** AgentCourt TypeScript declarations */

export interface Evidence {
  type: string;
  claimed_fact: string;
  source?: string;
  timestamp?: string;
}

export interface Ruling {
  caseId: string;
  status: string;
  matchedRule: string;
  remedy: string;
  confidence: 'high' | 'medium' | 'low';
  rulingText: string;
  reasoning: string;
  policyName: string;
  evidenceScores: Array<{ id: string; type: string; score: number }>;
  factsEstablished: Array<{ fact: string; value: string }>;
  factsDisputed: Array<{ fact: string; value: string }>;
  factsUnknown: Array<{ fact: string; reason: string }>;
  ruledAt: string;
  engineVersion: string;
  raw: Record<string, any>;
}

export interface ResolveParams {
  policy: string;
  claim: string;
  claimant: string;
  respondent: string;
  desiredRemedy?: string;
  evidence?: Evidence[];
  metadata?: Record<string, any>;
  contract?: Record<string, any>;
}

export interface PolicyInfo {
  name: string;
  version: string;
  description: string;
  rules_count: number;
}

export interface HealthInfo {
  status: string;
  version: string;
  engine: string;
  policies: string[];
}

export declare class AgentCourt {
  constructor(apiUrl?: string, timeout?: number);
  resolve(params: ResolveParams): Promise<Ruling>;
  listPolicies(): Promise<PolicyInfo[]>;
  getPolicy(name: string): Promise<PolicyInfo>;
  getVerdict(caseId: string): Promise<Ruling>;
  listVerdicts(): Promise<{ total: number; verdicts: Ruling[] }>;
  health(): Promise<HealthInfo>;
}

export declare function resolveDispute(params: ResolveParams): Promise<Ruling>;
