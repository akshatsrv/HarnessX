from typing import Any, Dict, List, Optional
from pydantic import BaseModel
from app.domain.claims import Claim
from app.domain.documents import ClaimDocument
from app.domain.risk import RiskAssessment
from app.domain.investigations import InvestigationReport
from app.domain.cases import InvestigationCase


class HealthResponse(BaseModel):
    status: str
    version: str
    environment: str
    services: Dict[str, str]


class ClaimListResponse(BaseModel):
    claims: List[Claim]
    total: int


class ClaimDetailResponse(BaseModel):
    claim: Claim
    documents: List[ClaimDocument]
    latest_risk: Optional[RiskAssessment] = None
    latest_investigation: Optional[InvestigationReport] = None
    associated_case: Optional[InvestigationCase] = None


class DocumentUploadResponse(BaseModel):
    document_id: str
    upload_url: str
    gcs_uri: str


class DocumentExtractionResponse(BaseModel):
    document_id: str
    status: str
    extracted_fields: Dict[str, Any]
