from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class CaseStatus(str, Enum):
    OPEN = "OPEN"
    UNDER_INVESTIGATION = "UNDER_INVESTIGATION"
    PENDING_INFORMATION = "PENDING_INFORMATION"
    APPROVED = "APPROVED"
    REFERRED_TO_LEGAL = "REFERRED_TO_LEGAL"
    CLOSED = "CLOSED"


class CaseNote(BaseModel):
    note_id: str
    author_id: str
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class InvestigationCase(BaseModel):
    case_id: str
    claim_id: str
    investigation_id: str
    status: CaseStatus = CaseStatus.UNDER_INVESTIGATION
    assigned_analyst_id: str
    notes: List[CaseNote] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
