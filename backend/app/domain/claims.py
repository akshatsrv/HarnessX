from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class ClaimStatus(str, Enum):
    SUBMITTED = "SUBMITTED"
    UNDER_REVIEW = "UNDER_REVIEW"
    UNDER_INVESTIGATION = "UNDER_INVESTIGATION"
    APPROVED = "APPROVED"
    REFERRED_TO_SIU = "REFERRED_TO_SIU"
    CLOSED = "CLOSED"


class Claim(BaseModel):
    claim_id: str
    customer_id: str
    vehicle_id: str
    incident_date: str
    claimed_amount: float
    currency: str = "INR"
    damage_reported: Optional[str] = None
    incident_location: Optional[str] = None
    status: ClaimStatus = ClaimStatus.SUBMITTED
    document_ids: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
