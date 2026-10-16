import pytest
from app.domain.claims import ClaimStatus
from app.repositories.claims_repository import ClaimsRepository
from app.schemas.requests import CreateClaimRequest
from app.services.claim_service import ClaimService


@pytest.mark.asyncio
async def test_create_and_fetch_claim():
    repo = ClaimsRepository()
    service = ClaimService(repo)

    req = CreateClaimRequest(
        customer_id="C-TEST-99",
        vehicle_id="V-99",
        incident_date="2026-10-10",
        claimed_amount=150000.0,
        damage_reported="Front bumper scratch"
    )

    created = await service.create_claim(req)
    assert created.claim_id.startswith("CLM-")
    assert created.status == ClaimStatus.SUBMITTED

    fetched = await service.get_claim(created.claim_id)
    assert fetched is not None
    assert fetched.customer_id == "C-TEST-99"
