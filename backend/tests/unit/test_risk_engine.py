# pyrefly: ignore[missing-import]
import pytest
from app.domain.claims import Claim
from app.domain.documents import ClaimDocument, DocumentType, ExtractionStatus
from app.domain.risk import RiskLevel
from app.risk.scoring import RiskScoringEngine


@pytest.mark.asyncio
async def test_risk_scoring_detects_mismatch_and_high_amount():
    engine = RiskScoringEngine()

    claim = Claim(
        claim_id="CLM-TEST-01",
        customer_id="C-TEST",
        vehicle_id="V-100",
        incident_date="2026-09-12",
        claimed_amount=485000.0
    )

    documents = [
        ClaimDocument(
            document_id="DOC-1",
            claim_id="CLM-TEST-01",
            file_name="claim.pdf",
            document_type=DocumentType.CLAIM_FORM,
            gcs_uri="gs://test/claim.pdf",
            extraction_status=ExtractionStatus.EXTRACTED,
            extracted_fields={"incident_date": "2026-09-12"}
        ),
        ClaimDocument(
            document_id="DOC-2",
            claim_id="CLM-TEST-01",
            file_name="fir.pdf",
            document_type=DocumentType.POLICE_REPORT,
            gcs_uri="gs://test/fir.pdf",
            extraction_status=ExtractionStatus.EXTRACTED,
            extracted_fields={"date_of_incident": "2026-09-14"}
        )
    ]

    historical_data = {
        "baseline_amount": 210000.0,
        "total_claims": 3,
        "claims_in_last_12_months": 2
    }

    assessment = await engine.compute_assessment(claim, documents, historical_data)

    assert assessment.score >= 70
    assert assessment.level == RiskLevel.HIGH
    signal_codes = [s.code for s in assessment.signals]
    assert "DOCUMENT_DATE_MISMATCH" in signal_codes
    assert "REPAIR_ESTIMATE_ANOMALY" in signal_codes
    assert "UNUSUAL_CLAIM_FREQUENCY" in signal_codes
