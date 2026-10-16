export type RiskLevel = 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
export type SignalSeverity = 'LOW' | 'MEDIUM' | 'HIGH';

export interface RiskSignal {
  code: string;
  severity: SignalSeverity;
  points: number;
  title: string;
  description: string;
  source_document_ids: string[];
  metadata?: Record<string, any>;
}

export interface RiskAssessment {
  assessment_id: string;
  claim_id: string;
  score: number;
  level: RiskLevel;
  rules_version: string;
  signals: RiskSignal[];
  assessed_at: string;
}
