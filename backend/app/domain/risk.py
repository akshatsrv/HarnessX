from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class SignalSeverity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class RiskSignal(BaseModel):
    code: str
    severity: SignalSeverity
    points: int
    title: str
    description: str
    source_document_ids: List[str] = Field(default_factory=list)
    metadata: dict = Field(default_factory=dict)


class RiskAssessment(BaseModel):
    assessment_id: str
    claim_id: str
    score: int
    level: RiskLevel
    rules_version: str = "v1"
    signals: List[RiskSignal] = Field(default_factory=list)
    assessed_at: datetime = Field(default_factory=datetime.utcnow)
