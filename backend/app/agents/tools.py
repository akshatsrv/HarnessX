from typing import Any, Dict, List
from app.domain.investigations import Finding, PolicyReference
from app.integrations.google_cloud.bigquery_client import BigQueryClient
from app.repositories.claims_repository import ClaimsRepository
from app.repositories.documents_repository import DocumentsRepository
from app.retrieval.policy_search import PolicySearchRetriever


class InvestigationTools:
    """Approved tools exposed to Gemini during claims investigation orchestration."""

    def __init__(
        self,
        claims_repo: ClaimsRepository,
        docs_repo: DocumentsRepository,
        bq_client: BigQueryClient,
        policy_retriever: PolicySearchRetriever
    ):
        self.claims_repo = claims_repo
        self.docs_repo = docs_repo
        self.bq_client = bq_client
        self.policy_retriever = policy_retriever

    async def get_claim_details(self, claim_id: str) -> Dict[str, Any]:
        """Tool: get_claim_details(claim_id)"""
        claim = await self.claims_repo.get_by_id(claim_id)
        return claim.model_dump() if claim else {}

    async def get_customer_claim_history(self, customer_id: str) -> Dict[str, Any]:
        """Tool: get_customer_claim_history(customer_id)"""
        return await self.bq_client.get_customer_claim_history(customer_id)

    async def get_repair_estimate_baseline(self, claim_type: str, vehicle_type: str) -> Dict[str, Any]:
        """Tool: get_repair_estimate_baseline(claim_type, vehicle_type)"""
        return await self.bq_client.get_repair_baseline(vehicle_type, claim_type)

    async def get_document_extraction(self, document_id: str) -> Dict[str, Any]:
        """Tool: get_document_extraction(document_id)"""
        doc = await self.docs_repo.get_by_id(document_id)
        return doc.extracted_fields if doc else {}

    async def search_insurance_policy(self, query: str, claim_type: str = "motor") -> List[Dict[str, Any]]:
        """Tool: search_insurance_policy(query, claim_type)"""
        refs = await self.policy_retriever.search_applicable_policies(query, claim_type)
        return [r.model_dump() for r in refs]
