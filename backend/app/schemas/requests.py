from typing import Optional
from pydantic import BaseModel
from app.domain.cases import CaseStatus
from app.domain.documents import DocumentType


class CreateClaimRequest(BaseModel):
    customer_id: str
    vehicle_id: str
    incident_date: str
    claimed_amount: float
    currency: str = "INR"
    damage_reported: Optional[str] = None
    incident_location: Optional[str] = None


class RegisterDocumentRequest(BaseModel):
    file_name: str
    document_type: DocumentType
    content_type: str = "application/pdf"


class AssessRiskRequest(BaseModel):
    recompute: bool = False


class StartInvestigationRequest(BaseModel):
    include_policy_search: bool = True
    include_historical_analytics: bool = True


class CreateCaseRequest(BaseModel):
    investigation_id: str
    assigned_analyst_id: Optional[str] = "ANALYST-001"
    initial_note: Optional[str] = None


class UpdateCaseRequest(BaseModel):
    status: Optional[CaseStatus] = None
    add_note: Optional[str] = None
