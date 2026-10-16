from fastapi import APIRouter, Depends, HTTPException
from app.api.dependencies import get_investigation_service
from app.core.security import get_current_analyst
from app.domain.investigations import InvestigationReport
from app.services.investigation_service import InvestigationService

router = APIRouter(prefix="/investigations", tags=["Investigations"])


@router.get("/{investigation_id}", response_model=InvestigationReport)
async def get_investigation_report(
    investigation_id: str,
    inv_service: InvestigationService = Depends(get_investigation_service),
    current_analyst: dict = Depends(get_current_analyst)
):
    report = await inv_service.get_investigation_report(investigation_id)
    if not report:
        raise HTTPException(status_code=404, detail=f"Investigation '{investigation_id}' not found")
    return report
