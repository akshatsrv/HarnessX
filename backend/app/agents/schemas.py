from typing import List, Optional
from pydantic import BaseModel, Field


class ToolCallRecord(BaseModel):
    tool_name: str
    arguments: dict
    output: dict


class AgentInvestigationContext(BaseModel):
    claim_id: str
    customer_id: str
    vehicle_id: str
    claimed_amount: float
    documents_extracted: List[dict] = Field(default_factory=list)
    risk_signals: List[dict] = Field(default_factory=list)
    risk_score: int
    historical_claim_data: dict = Field(default_factory=dict)
    repair_baseline_data: dict = Field(default_factory=dict)
    applicable_policies: List[dict] = Field(default_factory=list)
