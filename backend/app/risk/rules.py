from typing import List, Optional
from app.domain.claims import Claim
from app.domain.documents import ClaimDocument
from app.domain.risk import RiskSignal, SignalSeverity


class BaseRule:
    rule_code: str = ""
    title: str = ""
    severity: SignalSeverity = SignalSeverity.LOW
    points: int = 0

    async def evaluate(
        self,
        claim: Claim,
        documents: List[ClaimDocument],
        historical_data: dict
    ) -> Optional[RiskSignal]:
        raise NotImplementedError


class DocumentDateMismatchRule(BaseRule):
    rule_code = "DOCUMENT_DATE_MISMATCH"
    title = "Discrepancy in Reported Incident Dates"
    severity = SignalSeverity.MEDIUM
    points = 15

    async def evaluate(self, claim: Claim, documents: List[ClaimDocument], historical_data: dict) -> Optional[RiskSignal]:
        # Cross-reference claim form date vs police report date
        dates = {}
        source_doc_ids = []
        for doc in documents:
            if doc.extracted_fields.get("incident_date"):
                dates["claim_form"] = doc.extracted_fields["incident_date"]
                source_doc_ids.append(doc.document_id)
            if doc.extracted_fields.get("date_of_incident"):
                dates["police_report"] = doc.extracted_fields["date_of_incident"]
                source_doc_ids.append(doc.document_id)

        if "claim_form" in dates and "police_report" in dates:
            if dates["claim_form"] != dates["police_report"]:
                return RiskSignal(
                    code=self.rule_code,
                    title=self.title,
                    severity=self.severity,
                    points=self.points,
                    description=f"Claim intimation states {dates['claim_form']} while Police FIR states {dates['police_report']}.",
                    source_document_ids=source_doc_ids,
                    metadata={"dates_found": dates}
                )
        return None


class RepairEstimateAnomalyRule(BaseRule):
    rule_code = "REPAIR_ESTIMATE_ANOMALY"
    title = "Repair Estimate Substantially Above Benchmark"
    severity = SignalSeverity.HIGH
    points = 20

    async def evaluate(self, claim: Claim, documents: List[ClaimDocument], historical_data: dict) -> Optional[RiskSignal]:
        baseline = historical_data.get("baseline_amount", 210000.0)
        claimed = claim.claimed_amount
        if claimed > baseline * 1.5:  # Over 50% above benchmark
            variance = int(((claimed - baseline) / baseline) * 100)
            return RiskSignal(
                code=self.rule_code,
                title=self.title,
                severity=self.severity,
                points=self.points,
                description=f"Claimed amount of ₹{claimed:,.0f} exceeds comparable damage baseline (₹{baseline:,.0f}) by {variance}%.",
                source_document_ids=[doc.document_id for doc in documents if doc.document_type == "REPAIR_ESTIMATE"],
                metadata={"claimed": claimed, "baseline": baseline, "variance_pct": variance}
            )
        return None


class CustomerClaimFrequencyRule(BaseRule):
    rule_code = "UNUSUAL_CLAIM_FREQUENCY"
    title = "Repeated Customer Claims in Historical Window"
    severity = SignalSeverity.HIGH
    points = 20

    async def evaluate(self, claim: Claim, documents: List[ClaimDocument], historical_data: dict) -> Optional[RiskSignal]:
        total_claims = historical_data.get("total_claims", 0)
        recent_claims = historical_data.get("claims_in_last_12_months", 0)
        if recent_claims >= 2:
            return RiskSignal(
                code=self.rule_code,
                title=self.title,
                severity=self.severity,
                points=self.points,
                description=f"Customer has submitted {total_claims} claims in total ({recent_claims} claims within the last 12 months).",
                metadata={"total_claims": total_claims, "recent_claims": recent_claims}
            )
        return None


class HighClaimAmountRule(BaseRule):
    rule_code = "HIGH_CLAIM_AMOUNT"
    title = "Claim Amount Exceeds Standard Threshold"
    severity = SignalSeverity.MEDIUM
    points = 15

    async def evaluate(self, claim: Claim, documents: List[ClaimDocument], historical_data: dict) -> Optional[RiskSignal]:
        if claim.claimed_amount >= 300000:
            return RiskSignal(
                code=self.rule_code,
                title=self.title,
                severity=self.severity,
                points=self.points,
                description=f"Claimed amount of ₹{claim.claimed_amount:,.0f} exceeds the automatic settlement ceiling.",
                metadata={"claimed_amount": claim.claimed_amount}
            )
        return None


class PolicyMandatoryInspectionRule(BaseRule):
    rule_code = "POLICY_INSPECTION_CONDITION"
    title = "Policy Threshold Triggering Mandatory In-Person Survey"
    severity = SignalSeverity.LOW
    points = 10

    async def evaluate(self, claim: Claim, documents: List[ClaimDocument], historical_data: dict) -> Optional[RiskSignal]:
        if claim.claimed_amount >= 250000:
            return RiskSignal(
                code=self.rule_code,
                title=self.title,
                severity=self.severity,
                points=self.points,
                description="Policy section 4.1 mandates independent physical surveyor inspection for claims exceeding ₹2,50,000.",
                metadata={"policy_clause": "POL-MOT-2026-V1 Sec 4.1"}
            )
        return None
