import uuid
from typing import List
from app.domain.claims import Claim
from app.domain.documents import ClaimDocument
from app.domain.risk import RiskAssessment, RiskLevel, RiskSignal
from app.risk.rules import (
    CustomerClaimFrequencyRule,
    DocumentDateMismatchRule,
    HighClaimAmountRule,
    PolicyMandatoryInspectionRule,
    RepairEstimateAnomalyRule,
)


class RiskScoringEngine:
    """Executes rule chain and aggregates deterministic score."""

    def __init__(self):
        self.rules = [
            DocumentDateMismatchRule(),
            RepairEstimateAnomalyRule(),
            CustomerClaimFrequencyRule(),
            HighClaimAmountRule(),
            PolicyMandatoryInspectionRule(),
        ]

    async def compute_assessment(
        self,
        claim: Claim,
        documents: List[ClaimDocument],
        historical_data: dict
    ) -> RiskAssessment:
        signals: List[RiskSignal] = []
        total_score = 0

        for rule in self.rules:
            signal = await rule.evaluate(claim, documents, historical_data)
            if signal:
                signals.append(signal)
                total_score += signal.points

        # Cap score at 100
        score = min(total_score, 100)

        # Classify Level
        if score >= 75:
            level = RiskLevel.HIGH
        elif score >= 40:
            level = RiskLevel.MEDIUM
        else:
            level = RiskLevel.LOW

        return RiskAssessment(
            assessment_id=f"RISK-{uuid.uuid4().hex[:8].upper()}",
            claim_id=claim.claim_id,
            score=score,
            level=level,
            rules_version="v1",
            signals=signals
        )
