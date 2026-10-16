export type CaseStatus =
  | 'OPEN'
  | 'UNDER_INVESTIGATION'
  | 'PENDING_INFORMATION'
  | 'APPROVED'
  | 'REFERRED_TO_LEGAL'
  | 'CLOSED';

export interface CaseNote {
  note_id: string;
  author_id: string;
  content: string;
  created_at: string;
}

export interface InvestigationCase {
  case_id: string;
  claim_id: string;
  investigation_id: string;
  status: CaseStatus;
  assigned_analyst_id: string;
  notes: CaseNote[];
  created_at: string;
  updated_at: string;
}
