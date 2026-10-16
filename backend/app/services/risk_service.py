from typing import Dict, Optional
from app.domain.risk import RiskAssessment
from app.integrations.google_cloud.bigquery_client import BigQueryClient
from app.repositories.claims_repository import ClaimsRepository
from app.repositories.documents_repository import DocumentsRepository
from app.risk.scoring import RiskScoringEngine


class RiskService:
    def __init__(
        self,
        claims_repo: ClaimsRepository,
        docs_repo: DocumentsRepository,
        bq_client: BigQueryClient,
        scoring_engine: RiskScoringEngine
    ):
        self.claims_repo = claims_repo
        self.docs_repo = docs_repo
        self.bq_client = bq_client
        self.scoring_engine = scoring_engine
        self._assessments: Dict[str, RiskAssessment] = {}

    async def assess_claim_risk(self, claim_id: str) -> Optional[RiskAssessment]:
        claim = await self.claims_repo.get_by_id(claim_id)
        if not claim:
            return None

        documents = await self.docs_repo.get_by_claim_id(claim_id)
        history = await self.bq_client.get_customer_claim_history(claim.customer_id)
        baseline = await self.bq_client.get_repair_baseline(
            vehicle_category=claim.vehicle_id,
            damage_type=claim.damage_reported or "Front collision"
        )

        combined_data = {**history, **baseline}
        assessment = await self.scoring_engine.compute_assessment(claim, documents, combined_data)
        self._assessments[claim_id] = assessment
        return assessment

    async def get_latest_assessment(self, claim_id: str) -> Optional[RiskAssessment]:
        return self._assessments.get(claim_id)
