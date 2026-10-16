import { Claim, ClaimDocument } from '../types/claim';
import { RiskAssessment } from '../types/risk';
import { InvestigationReport } from '../types/investigation';
import { InvestigationCase, CaseStatus } from '../types/case';

const API_BASE = '/api/v1';

export async function fetchClaims(): Promise<{ claims: Claim[]; total: number }> {
  const res = await fetch(`${API_BASE}/claims`);
  if (!res.ok) throw new Error('Failed to fetch claims');
  return res.json();
}

export async function fetchClaimDetails(claimId: string): Promise<{
  claim: Claim;
  documents: ClaimDocument[];
  latest_risk?: RiskAssessment;
  latest_investigation?: InvestigationReport;
  associated_case?: InvestigationCase;
}> {
  const res = await fetch(`${API_BASE}/claims/${claimId}`);
  if (!res.ok) throw new Error(`Failed to fetch details for ${claimId}`);
  return res.json();
}

export async function assessRisk(claimId: string): Promise<RiskAssessment> {
  const res = await fetch(`${API_BASE}/claims/${claimId}/assess-risk`, {
    method: 'POST'
  });
  if (!res.ok) throw new Error('Failed to calculate risk assessment');
  return res.json();
}

export async function triggerInvestigation(claimId: string): Promise<InvestigationReport> {
  const res = await fetch(`${API_BASE}/claims/${claimId}/investigations`, {
    method: 'POST'
  });
  if (!res.ok) throw new Error('Failed to run AI investigation');
  return res.json();
}

export async function createCase(
  claimId: string,
  investigationId: string,
  initialNote?: string
): Promise<InvestigationCase> {
  const res = await fetch(`${API_BASE}/claims/${claimId}/cases`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      investigation_id: investigationId,
      initial_note: initialNote
    })
  });
  if (!res.ok) throw new Error('Failed to create investigation case');
  return res.json();
}

export async function updateCaseStatus(
  caseId: string,
  status?: CaseStatus,
  addNote?: string
): Promise<InvestigationCase> {
  const res = await fetch(`${API_BASE}/cases/${caseId}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ status, add_note: addNote })
  });
  if (!res.ok) throw new Error('Failed to update case');
  return res.json();
}
