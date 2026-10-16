from typing import Dict, List, Optional
from app.domain.claims import Claim, ClaimStatus


class ClaimsRepository:
    """In-memory demo store preloaded with seeded synthetic claims, expandable to Firestore/SQL."""

    def __init__(self):
        self._claims: Dict[str, Claim] = {
            "CLM-10291": Claim(
                claim_id="CLM-10291",
                customer_id="C10291",
                vehicle_id="V-301",
                incident_date="2026-09-12",
                claimed_amount=485000.0,
                currency="INR",
                damage_reported="Front bumper, headlight, bonnet",
                incident_location="Delhi Outer Ring Road",
                status=ClaimStatus.SUBMITTED,
                document_ids=["DOC-101", "DOC-102", "DOC-103", "DOC-104"]
            ),
            "CLM-10292": Claim(
                claim_id="CLM-10292",
                customer_id="C10292",
                vehicle_id="V-302",
                incident_date="2026-10-01",
                claimed_amount=25000.0,
                currency="INR",
                damage_reported="Rear bumper scratch",
                incident_location="Bengaluru",
                status=ClaimStatus.APPROVED,
                document_ids=["DOC-201"]
            ),
            "CLM-10293": Claim(
                claim_id="CLM-10293",
                customer_id="C10293",
                vehicle_id="V-303",
                incident_date="2026-09-28",
                claimed_amount=180000.0,
                currency="INR",
                damage_reported="Side door dent and suspension damage",
                incident_location="Mumbai",
                status=ClaimStatus.UNDER_INVESTIGATION,
                document_ids=["DOC-301", "DOC-302"]
            )
        }

    async def get_all(self) -> List[Claim]:
        return list(self._claims.values())

    async def get_by_id(self, claim_id: str) -> Optional[Claim]:
        return self._claims.get(claim_id)

    async def save(self, claim: Claim) -> Claim:
        self._claims[claim.claim_id] = claim
        return claim
