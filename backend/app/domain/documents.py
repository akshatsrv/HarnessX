from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class DocumentType(str, Enum):
    CLAIM_FORM = "CLAIM_FORM"
    POLICE_REPORT = "POLICE_REPORT"
    REPAIR_ESTIMATE = "REPAIR_ESTIMATE"
    INSURANCE_POLICY = "INSURANCE_POLICY"
    PHOTO_EVIDENCE = "PHOTO_EVIDENCE"
    OTHER = "OTHER"


class ExtractionStatus(str, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    EXTRACTED = "EXTRACTED"
    FAILED = "FAILED"


class ClaimDocument(BaseModel):
    document_id: str
    claim_id: str
    file_name: str
    document_type: DocumentType
    gcs_uri: str
    extraction_status: ExtractionStatus = ExtractionStatus.PENDING
    extracted_fields: Dict[str, Any] = Field(default_factory=dict)
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)
