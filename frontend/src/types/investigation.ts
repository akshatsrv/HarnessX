export interface Finding {
  category: string;
  description: string;
  evidence_source: string;
  confidence: number;
}

export interface PolicyReference {
  document_title: string;
  section: string;
  quote: string;
  relevance: string;
}

export interface InvestigationReport {
  investigation_id: string;
  claim_id: string;
  status: string;
  risk_assessment_id?: string;
  summary: string;
  findings: Finding[];
  policy_references: PolicyReference[];
  uncertainties: string[];
  recommended_actions: string[];
  model_id: string;
  prompt_version: string;
  created_at: string;
}
