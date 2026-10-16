export type ClaimStatus =
  | 'SUBMITTED'
  | 'UNDER_REVIEW'
  | 'UNDER_INVESTIGATION'
  | 'APPROVED'
  | 'REFERRED_TO_SIU'
  | 'CLOSED';

export interface Claim {
  claim_id: string;
  customer_id: string;
  vehicle_id: string;
  incident_date: string;
  claimed_amount: number;
  currency: string;
  damage_reported?: string;
  incident_location?: string;
  status: ClaimStatus;
  document_ids: string[];
  created_at: string;
}

export interface ClaimDocument {
  document_id: string;
  claim_id: string;
  file_name: string;
  document_type: string;
  gcs_uri: string;
  extraction_status: string;
  extracted_fields: Record<string, any>;
  uploaded_at: string;
}
