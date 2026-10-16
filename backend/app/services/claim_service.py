import uuid
from typing import List, Optional
from app.domain.claims import Claim, ClaimStatus
from app.repositories.claims_repository import ClaimsRepository
from app.schemas.requests import CreateClaimRequest


class ClaimService:
    def __init__(self, claims_repo: ClaimsRepository):
        self.claims_repo = claims_repo

    async def list_claims(self) -> List[Claim]:
        return await self.claims_repo.get_all()

    async def get_claim(self, claim_id: str) -> Optional[Claim]:
        return await self.claims_repo.get_by_id(claim_id)

    async def create_claim(self, request: CreateClaimRequest) -> Claim:
        claim_id = f"CLM-{uuid.uuid4().hex[:6].upper()}"
        claim = Claim(
            claim_id=claim_id,
            customer_id=request.customer_id,
            vehicle_id=request.vehicle_id,
            incident_date=request.incident_date,
            claimed_amount=request.claimed_amount,
            currency=request.currency,
            damage_reported=request.damage_reported,
            incident_location=request.incident_location,
            status=ClaimStatus.SUBMITTED
        )
        return await self.claims_repo.save(claim)

    async def update_status(self, claim_id: str, new_status: ClaimStatus) -> Optional[Claim]:
        claim = await self.claims_repo.get_by_id(claim_id)
        if not claim:
            return None
        claim.status = new_status
        return await self.claims_repo.save(claim)
