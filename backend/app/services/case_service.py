import uuid
from datetime import datetime
from typing import List, Optional
from app.domain.cases import CaseNote, CaseStatus, InvestigationCase
from app.domain.claims import ClaimStatus
from app.repositories.cases_repository import CasesRepository
from app.repositories.claims_repository import ClaimsRepository
from app.schemas.requests import CreateCaseRequest, UpdateCaseRequest


class CaseService:
    def __init__(self, cases_repo: CasesRepository, claims_repo: ClaimsRepository):
        self.cases_repo = cases_repo
        self.claims_repo = claims_repo

    async def create_case(self, claim_id: str, request: CreateCaseRequest) -> InvestigationCase:
        case_id = f"CASE-{uuid.uuid4().hex[:6].upper()}"

        notes = []
        if request.initial_note:
            notes.append(CaseNote(
                note_id=f"NOTE-{uuid.uuid4().hex[:6].upper()}",
                author_id=request.assigned_analyst_id or "ANALYST-001",
                content=request.initial_note
            ))

        case = InvestigationCase(
            case_id=case_id,
            claim_id=claim_id,
            investigation_id=request.investigation_id,
            status=CaseStatus.UNDER_INVESTIGATION,
            assigned_analyst_id=request.assigned_analyst_id or "ANALYST-001",
            notes=notes
        )

        saved_case = await self.cases_repo.save(case)

        # Update associated claim status
        claim = await self.claims_repo.get_by_id(claim_id)
        if claim:
            claim.status = ClaimStatus.UNDER_INVESTIGATION
            await self.claims_repo.save(claim)

        return saved_case

    async def get_case(self, case_id: str) -> Optional[InvestigationCase]:
        return await self.cases_repo.get_by_id(case_id)

    async def get_case_by_claim(self, claim_id: str) -> Optional[InvestigationCase]:
        return await self.cases_repo.get_by_claim_id(claim_id)

    async def list_cases(self) -> List[InvestigationCase]:
        return await self.cases_repo.get_all()

    async def update_case(self, case_id: str, request: UpdateCaseRequest, analyst_id: str = "ANALYST-001") -> Optional[InvestigationCase]:
        case = await self.cases_repo.get_by_id(case_id)
        if not case:
            return None

        if request.status:
            case.status = request.status

        if request.add_note:
            case.notes.append(CaseNote(
                note_id=f"NOTE-{uuid.uuid4().hex[:6].upper()}",
                author_id=analyst_id,
                content=request.add_note
            ))

        case.updated_at = datetime.utcnow()
        return await self.cases_repo.save(case)
