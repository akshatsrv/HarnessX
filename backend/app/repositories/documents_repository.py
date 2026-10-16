from typing import Dict, List, Optional
from app.domain.documents import ClaimDocument, DocumentType, ExtractionStatus


class DocumentsRepository:
    """Manages claim documents, metadata, and extracted entities."""

    def __init__(self):
        self._documents: Dict[str, ClaimDocument] = {
            "DOC-101": ClaimDocument(
                document_id="DOC-101",
                claim_id="CLM-10291",
                file_name="claim_form.pdf",
                document_type=DocumentType.CLAIM_FORM,
                gcs_uri="gs://claimguard-claims-documents/claims/CLM-10291/claim_form.pdf",
                extraction_status=ExtractionStatus.EXTRACTED,
                extracted_fields={
                    "claim_id": "CLM-10291",
                    "incident_date": "2026-09-12",
                    "claimed_amount": 485000,
                    "customer_name": "Rajesh Kumar"
                }
            ),
            "DOC-102": ClaimDocument(
                document_id="DOC-102",
                claim_id="CLM-10291",
                file_name="police_report.pdf",
                document_type=DocumentType.POLICE_REPORT,
                gcs_uri="gs://claimguard-claims-documents/claims/CLM-10291/police_report.pdf",
                extraction_status=ExtractionStatus.EXTRACTED,
                extracted_fields={
                    "fir_number": "FIR-2026-8812",
                    "date_of_incident": "2026-09-14",
                    "incident_location": "Outer Ring Road, Near Rohini, Delhi"
                }
            ),
            "DOC-103": ClaimDocument(
                document_id="DOC-103",
                claim_id="CLM-10291",
                file_name="repair_estimate.pdf",
                document_type=DocumentType.REPAIR_ESTIMATE,
                gcs_uri="gs://claimguard-claims-documents/claims/CLM-10291/repair_estimate.pdf",
                extraction_status=ExtractionStatus.EXTRACTED,
                extracted_fields={
                    "workshop": "Apex Auto Care Center, Delhi",
                    "total_estimate": 485000,
                    "estimate_date": "2026-09-15"
                }
            ),
            "DOC-104": ClaimDocument(
                document_id="DOC-104",
                claim_id="CLM-10291",
                file_name="insurance_policy.pdf",
                document_type=DocumentType.INSURANCE_POLICY,
                gcs_uri="gs://claimguard-claims-documents/claims/CLM-10291/insurance_policy.pdf",
                extraction_status=ExtractionStatus.EXTRACTED,
                extracted_fields={
                    "policy_number": "POL-MOT-2026-V1",
                    "coverage": "Comprehensive Private Car"
                }
            )
        }

    async def get_by_id(self, document_id: str) -> Optional[ClaimDocument]:
        return self._documents.get(document_id)

    async def get_by_claim_id(self, claim_id: str) -> List[ClaimDocument]:
        return [doc for doc in self._documents.values() if doc.claim_id == claim_id]

    async def save(self, document: ClaimDocument) -> ClaimDocument:
        self._documents[document.document_id] = document
        return document
