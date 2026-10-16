from typing import Dict, List, Optional
from app.domain.cases import InvestigationCase


class CasesRepository:
    """Manages Investigation Cases in Firestore with in-memory fallback for local development."""

    def __init__(self):
        self._cases: Dict[str, InvestigationCase] = {}

    async def get_by_id(self, case_id: str) -> Optional[InvestigationCase]:
        return self._cases.get(case_id)

    async def get_by_claim_id(self, claim_id: str) -> Optional[InvestigationCase]:
        for case in self._cases.values():
            if case.claim_id == claim_id:
                return case
        return None

    async def get_all(self) -> List[InvestigationCase]:
        return list(self._cases.values())

    async def save(self, case: InvestigationCase) -> InvestigationCase:
        self._cases[case.case_id] = case
        return case
