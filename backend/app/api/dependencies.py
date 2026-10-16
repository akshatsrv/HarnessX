from app.agents.investigator import InvestigationAgent
from app.agents.tools import InvestigationTools
from app.integrations.google_cloud.bigquery_client import BigQueryClient
from app.integrations.google_cloud.document_ai_client import DocumentAIClient
from app.integrations.google_cloud.storage_client import StorageClient
from app.integrations.google_cloud.vertex_ai_client import VertexAIClient
from app.repositories.cases_repository import CasesRepository
from app.repositories.claims_repository import ClaimsRepository
from app.repositories.documents_repository import DocumentsRepository
from app.retrieval.policy_search import PolicySearchRetriever
from app.risk.scoring import RiskScoringEngine
from app.services.case_service import CaseService
from app.services.claim_service import ClaimService
from app.services.document_service import DocumentService
from app.services.investigation_service import InvestigationService
from app.services.risk_service import RiskService

# Singleton instances for repository and service lifecycle
claims_repo = ClaimsRepository()
cases_repo = CasesRepository()
docs_repo = DocumentsRepository()

bq_client = BigQueryClient()
docai_client = DocumentAIClient()
storage_client = StorageClient()
vertex_client = VertexAIClient()

policy_retriever = PolicySearchRetriever()
scoring_engine = RiskScoringEngine()

claim_service = ClaimService(claims_repo)
doc_service = DocumentService(docs_repo, claims_repo, storage_client, docai_client)
risk_service = RiskService(claims_repo, docs_repo, bq_client, scoring_engine)

investigation_tools = InvestigationTools(claims_repo, docs_repo, bq_client, policy_retriever)
investigation_agent = InvestigationAgent(investigation_tools, vertex_client)
investigation_service = InvestigationService(claims_repo, risk_service, investigation_agent)
case_service = CaseService(cases_repo, claims_repo)


def get_claim_service() -> ClaimService:
    return claim_service


def get_doc_service() -> DocumentService:
    return doc_service


def get_risk_service() -> RiskService:
    return risk_service


def get_investigation_service() -> InvestigationService:
    return investigation_service


def get_case_service() -> CaseService:
    return case_service
