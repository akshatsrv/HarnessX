from typing import Dict, Optional
from app.agents.investigator import InvestigationAgent
from app.domain.claims import ClaimStatus
from app.domain.investigations import InvestigationReport
from app.repositories.claims_repository import ClaimsRepository
from app.services.risk_service import RiskService


class InvestigationService:
    def __init__(
        self,
        claims_repo: ClaimsRepository,
        risk_service: RiskService,
        agent: InvestigationAgent
    ):
        self.claims_repo = claims_repo
        self.risk_service = risk_service
        self.agent = agent
        self._reports: Dict[str, InvestigationReport] = {}

    async def start_investigation(self, claim_id: str) -> Optional[InvestigationReport]:
        claim = await self.claims_repo.get_by_id(claim_id)
        if not claim:
            return None

        # Ensure risk assessment exists
        risk_assessment = await self.risk_service.assess_claim_risk(claim_id)

        # Run Gemini investigation agent
        report = await self.agent.run_investigation(claim, risk_assessment)
        self._reports[report.investigation_id] = report
        self._reports[claim_id] = report  # Index by both ID and claim

        # Update claim status
        claim.status = ClaimStatus.UNDER_INVESTIGATION
        await self.claims_repo.save(claim)

        return report

    async def get_investigation_report(self, identifier: str) -> Optional[InvestigationReport]:
        return self._reports.get(identifier)
