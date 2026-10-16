from fastapi import APIRouter, Depends, HTTPException, status
from app.api.dependencies import (
    get_case_service,
    get_claim_service,
    get_doc_service,
    get_investigation_service,
    get_risk_service,
)
from app.core.security import get_current_analyst
from app.domain.claims import Claim
from app.domain.cases import InvestigationCase
from app.domain.investigations import InvestigationReport
from app.domain.risk import RiskAssessment
from app.schemas.requests import (
    CreateCaseRequest,
    CreateClaimRequest,
    RegisterDocumentRequest,
)
from app.schemas.responses import (
    ClaimDetailResponse,
    ClaimListResponse,
    DocumentUploadResponse,
)
from app.services.case_service import CaseService
from app.services.claim_service import ClaimService
from app.services.document_service import DocumentService
from app.services.investigation_service import InvestigationService
from app.services.risk_service import RiskService

router = APIRouter(prefix="/claims", tags=["Claims"])


@router.get("", response_model=ClaimListResponse)
async def list_claims(
    claim_service: ClaimService = Depends(get_claim_service),
    current_analyst: dict = Depends(get_current_analyst)
):
    claims = await claim_service.list_claims()
    return ClaimListResponse(claims=claims, total=len(claims))


@router.post("", response_model=Claim, status_code=status.HTTP_201_CREATED)
async def create_claim(
    request: CreateClaimRequest,
    claim_service: ClaimService = Depends(get_claim_service),
    current_analyst: dict = Depends(get_current_analyst)
):
    return await claim_service.create_claim(request)


@router.get("/{claim_id}", response_model=ClaimDetailResponse)
async def get_claim_details(
    claim_id: str,
    claim_service: ClaimService = Depends(get_claim_service),
    doc_service: DocumentService = Depends(get_doc_service),
    risk_service: RiskService = Depends(get_risk_service),
    inv_service: InvestigationService = Depends(get_investigation_service),
    case_service: CaseService = Depends(get_case_service),
    current_analyst: dict = Depends(get_current_analyst)
):
    claim = await claim_service.get_claim(claim_id)
    if not claim:
        raise HTTPException(status_code=404, detail=f"Claim '{claim_id}' not found")

    documents = await doc_service.get_claim_documents(claim_id)
    latest_risk = await risk_service.get_latest_assessment(claim_id)
    latest_inv = await inv_service.get_investigation_report(claim_id)
    associated_case = await case_service.get_case_by_claim(claim_id)

    return ClaimDetailResponse(
        claim=claim,
        documents=documents,
        latest_risk=latest_risk,
        latest_investigation=latest_inv,
        associated_case=associated_case
    )


@router.post("/{claim_id}/documents", response_model=DocumentUploadResponse)
async def register_document(
    claim_id: str,
    request: RegisterDocumentRequest,
    doc_service: DocumentService = Depends(get_doc_service),
    current_analyst: dict = Depends(get_current_analyst)
):
    doc, upload_url = await doc_service.register_document(
        claim_id=claim_id,
        file_name=request.file_name,
        document_type=request.document_type,
        content_type=request.content_type
    )
    return DocumentUploadResponse(
        document_id=doc.document_id,
        upload_url=upload_url,
        gcs_uri=doc.gcs_uri
    )


@router.post("/{claim_id}/assess-risk", response_model=RiskAssessment)
async def assess_claim_risk(
    claim_id: str,
    risk_service: RiskService = Depends(get_risk_service),
    current_analyst: dict = Depends(get_current_analyst)
):
    assessment = await risk_service.assess_claim_risk(claim_id)
    if not assessment:
        raise HTTPException(status_code=404, detail=f"Claim '{claim_id}' not found")
    return assessment


@router.post("/{claim_id}/investigations", response_model=InvestigationReport)
async def run_investigation(
    claim_id: str,
    inv_service: InvestigationService = Depends(get_investigation_service),
    current_analyst: dict = Depends(get_current_analyst)
):
    report = await inv_service.start_investigation(claim_id)
    if not report:
        raise HTTPException(status_code=404, detail=f"Claim '{claim_id}' not found")
    return report


@router.post("/{claim_id}/cases", response_model=InvestigationCase, status_code=status.HTTP_201_CREATED)
async def create_case(
    claim_id: str,
    request: CreateCaseRequest,
    case_service: CaseService = Depends(get_case_service),
    current_analyst: dict = Depends(get_current_analyst)
):
    return await case_service.create_case(claim_id, request)
