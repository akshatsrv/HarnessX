import uuid
from typing import List, Optional, Tuple
from app.domain.documents import ClaimDocument, DocumentType, ExtractionStatus
from app.integrations.google_cloud.document_ai_client import DocumentAIClient
from app.integrations.google_cloud.storage_client import StorageClient
from app.repositories.claims_repository import ClaimsRepository
from app.repositories.documents_repository import DocumentsRepository


class DocumentService:
    def __init__(
        self,
        docs_repo: DocumentsRepository,
        claims_repo: ClaimsRepository,
        storage_client: StorageClient,
        docai_client: DocumentAIClient
    ):
        self.docs_repo = docs_repo
        self.claims_repo = claims_repo
        self.storage_client = storage_client
        self.docai_client = docai_client

    async def register_document(
        self,
        claim_id: str,
        file_name: str,
        document_type: DocumentType,
        content_type: str = "application/pdf"
    ) -> Tuple[ClaimDocument, str]:
        upload_url, gcs_uri = await self.storage_client.generate_upload_url(claim_id, file_name, content_type)
        doc_id = f"DOC-{uuid.uuid4().hex[:6].upper()}"

        doc = ClaimDocument(
            document_id=doc_id,
            claim_id=claim_id,
            file_name=file_name,
            document_type=document_type,
            gcs_uri=gcs_uri,
            extraction_status=ExtractionStatus.PENDING
        )
        saved_doc = await self.docs_repo.save(doc)

        claim = await self.claims_repo.get_by_id(claim_id)
        if claim and doc_id not in claim.document_ids:
            claim.document_ids.append(doc_id)
            await self.claims_repo.save(claim)

        return saved_doc, upload_url

    async def extract_document(self, document_id: str) -> Optional[ClaimDocument]:
        doc = await self.docs_repo.get_by_id(document_id)
        if not doc:
            return None

        fields = await self.docai_client.extract_document_fields(
            gcs_uri=doc.gcs_uri,
            document_type=doc.document_type,
            document_id=doc.document_id
        )

        doc.extracted_fields = fields
        doc.extraction_status = ExtractionStatus.EXTRACTED
        return await self.docs_repo.save(doc)

    async def get_claim_documents(self, claim_id: str) -> List[ClaimDocument]:
        return await self.docs_repo.get_by_claim_id(claim_id)
