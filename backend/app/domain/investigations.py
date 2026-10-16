from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class InvestigationStatus(str, Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class Finding(BaseModel):
    category: str
    description: str
    evidence_source: str
    confidence: float = 1.0


class PolicyReference(BaseModel):
    document_title: str
    section: str
    quote: str
    relevance: str


class InvestigationReport(BaseModel):
    investigation_id: str
    claim_id: str
    status: InvestigationStatus = InvestigationStatus.COMPLETED
    risk_assessment_id: Optional[str] = None
    summary: str
    findings: List[Finding] = Field(default_factory=list)
    policy_references: List[PolicyReference] = Field(default_factory=list)
    uncertainties: List[str] = Field(default_factory=list)
    recommended_actions: List[str] = Field(default_factory=list)
    model_id: str = "gemini-1.5-pro"
    prompt_version: str = "investigation-v1"
    created_at: datetime = Field(default_factory=datetime.utcnow)
