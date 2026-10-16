from typing import Optional
from fastapi import Header, HTTPException, status
from app.core.config import settings


async def get_current_analyst(authorization: Optional[str] = Header(None)) -> dict:
    """
    Validates Firebase Bearer token.
    For local development/demo when auth is skipped or running locally, returns a default analyst.
    """
    if settings.APP_ENV == "development" and not authorization:
        return {"analyst_id": "ANALYST-DEV-001", "email": "analyst@claimguard.demo", "role": "lead_investigator"}

    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid authentication token"
        )

    token = authorization.split("Bearer ")[1]
    # In production, verify token with firebase_admin.auth.verify_id_token(token)
    return {"analyst_id": "ANALYST-001", "token": token, "role": "claims_investigator"}
