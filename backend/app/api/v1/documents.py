from fastapi import APIRouter, Depends, HTTPException
from app.api.dependencies import get_doc_service
from app.core.security import get_current_analyst
from app.domain.documents import ClaimDocument
from app.schemas.responses import DocumentExtractionResponse
from app.services.document_service import DocumentService

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.post("/{document_id}/extract", response_model=DocumentExtractionResponse)
async def extract_document_fields(
    document_id: str,
    doc_service: DocumentService = Depends(get_doc_service),
    current_analyst: dict = Depends(get_current_analyst)
):
    doc = await doc_service.extract_document(document_id)
    if not doc:
        raise HTTPException(status_code=404, detail=f"Document '{document_id}' not found")
    return DocumentExtractionResponse(
        document_id=doc.document_id,
        status=doc.extraction_status.value,
        extracted_fields=doc.extracted_fields
    )


@router.get("/{document_id}", response_model=ClaimDocument)
async def get_document(
    document_id: str,
    doc_service: DocumentService = Depends(get_doc_service),
    current_analyst: dict = Depends(get_current_analyst)
):
    doc = await doc_service.docs_repo.get_by_id(document_id)
    if not doc:
        raise HTTPException(status_code=404, detail=f"Document '{document_id}' not found")
    return doc
