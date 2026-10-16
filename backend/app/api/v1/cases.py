from typing import List
from fastapi import APIRouter, Depends, HTTPException
from app.api.dependencies import get_case_service
from app.core.security import get_current_analyst
from app.domain.cases import InvestigationCase
from app.schemas.requests import UpdateCaseRequest
from app.services.case_service import CaseService

router = APIRouter(prefix="/cases", tags=["Cases"])


@router.get("", response_model=List[InvestigationCase])
async def list_cases(
    case_service: CaseService = Depends(get_case_service),
    current_analyst: dict = Depends(get_current_analyst)
):
    return await case_service.list_cases()


@router.get("/{case_id}", response_model=InvestigationCase)
async def get_case(
    case_id: str,
    case_service: CaseService = Depends(get_case_service),
    current_analyst: dict = Depends(get_current_analyst)
):
    case = await case_service.get_case(case_id)
    if not case:
        raise HTTPException(status_code=404, detail=f"Case '{case_id}' not found")
    return case


@router.patch("/{case_id}", response_model=InvestigationCase)
async def update_case(
    case_id: str,
    request: UpdateCaseRequest,
    case_service: CaseService = Depends(get_case_service),
    current_analyst: dict = Depends(get_current_analyst)
):
    case = await case_service.update_case(
        case_id=case_id,
        request=request,
        analyst_id=current_analyst.get("analyst_id", "ANALYST-001")
    )
    if not case:
        raise HTTPException(status_code=404, detail=f"Case '{case_id}' not found")
    return case
