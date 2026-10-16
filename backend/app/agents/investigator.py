import uuid
from app.agents.tools import InvestigationTools
from app.core.logging import logger
from app.domain.claims import Claim
from app.domain.investigations import Finding, InvestigationReport, InvestigationStatus, PolicyReference
from app.domain.risk import RiskAssessment
from app.integrations.google_cloud.vertex_ai_client import VertexAIClient


class InvestigationAgent:
    """Orchestrates Gemini-powered claims investigation workflow using approved tools."""

    def __init__(self, tools: InvestigationTools, vertex_client: VertexAIClient):
        self.tools = tools
        self.vertex_client = vertex_client

    async def run_investigation(
        self,
        claim: Claim,
        risk_assessment: RiskAssessment
    ) -> InvestigationReport:
        logger.info(f"Starting agent investigation for claim: {claim.claim_id}")

        # Step 1: Tool executions
        claim_history = await self.tools.get_customer_claim_history(claim.customer_id)
        repair_baseline = await self.tools.get_repair_estimate_baseline(
            claim_type=claim.damage_reported or "Front bumper collision",
            vehicle_type=claim.vehicle_id
        )
        policies = await self.tools.search_insurance_policy(
            query=f"inspection threshold {claim.claimed_amount} date discrepancy",
            claim_type="motor"
        )

        # Step 2: Context assembly
        context = {
            "claim": claim.model_dump(),
            "risk_assessment": risk_assessment.model_dump(),
            "claim_history": claim_history,
            "repair_baseline": repair_baseline,
            "policies": policies
        }

        # Step 3: Vertex AI Gemini reasoning
        synthesis = await self.vertex_client.generate_investigation_synthesis(
            prompt=f"Investigate claim {claim.claim_id}",
            context=context
        )

        return InvestigationReport(
            investigation_id=f"INV-{uuid.uuid4().hex[:8].upper()}",
            claim_id=claim.claim_id,
            status=InvestigationStatus.COMPLETED,
            risk_assessment_id=risk_assessment.assessment_id,
            summary=synthesis.get("summary", "Investigation completed."),
            findings=[Finding(**f) for f in synthesis.get("findings", [])],
            policy_references=[PolicyReference(**p) for p in synthesis.get("policy_references", [])],
            uncertainties=synthesis.get("uncertainties", []),
            recommended_actions=synthesis.get("recommended_actions", []),
            model_id="gemini-1.5-pro",
            prompt_version="investigation-v1"
        )
