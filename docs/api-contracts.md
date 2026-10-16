# API Contracts: ClaimGuard AI

All endpoints are versioned under `/api/v1/`.

## Endpoints Summary

| Method | Endpoint | Purpose | Description |
|---|---|---|---|
| `GET` | `/api/v1/health` | Health Check | Service health and dependency checks |
| `GET` | `/api/v1/claims` | List Claims | Returns list of claims with risk summary |
| `POST` | `/api/v1/claims` | Create Claim | Registers a new submitted claim |
| `GET` | `/api/v1/claims/{claim_id}` | Claim Details | Detailed claim info, documents, and risk |
| `POST` | `/api/v1/claims/{claim_id}/documents` | Upload Document | Upload and register supporting claim document |
| `POST` | `/api/v1/documents/{document_id}/extract` | Extract Document | Trigger Document AI extraction |
| `POST` | `/api/v1/claims/{claim_id}/assess-risk` | Assess Risk | Compute deterministic explainable risk score |
| `POST` | `/api/v1/claims/{claim_id}/investigations` | Run Investigation | Trigger Gemini-orchestrated investigation |
| `GET` | `/api/v1/investigations/{investigation_id}` | Read Report | Retrieve investigation findings & evidence |
| `POST` | `/api/v1/claims/{claim_id}/cases` | Create Case | Promote claim/investigation to active case |
| `PATCH` | `/api/v1/cases/{case_id}` | Update Case | Update case status or append analyst notes |

## Schemas

### Claim Schema
```json
{
  "claim_id": "CLM-10291",
  "customer_id": "C10291",
  "vehicle_id": "V-301",
  "incident_date": "2026-09-12",
  "claimed_amount": 485000,
  "currency": "INR",
  "status": "SUBMITTED",
  "document_ids": ["DOC-001", "DOC-002"],
  "created_at": "2026-10-15T10:00:00Z"
}
```

### Risk Assessment Schema
```json
{
  "assessment_id": "RISK-0001",
  "claim_id": "CLM-10291",
  "score": 82,
  "level": "HIGH",
  "rules_version": "v1",
  "signals": [
    {
      "code": "DOCUMENT_DATE_MISMATCH",
      "severity": "MEDIUM",
      "description": "Dates differ between submitted documents",
      "source_document_ids": ["DOC-001", "DOC-002"]
    }
  ]
}
```
