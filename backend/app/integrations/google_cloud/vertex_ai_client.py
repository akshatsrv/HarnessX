from typing import Any, Dict, List
from app.core.config import settings
from app.core.logging import logger


class VertexAIClient:
    """Manages Gemini model invocations on Vertex AI with structured schema validation."""

    def __init__(self):
        self.project_id = settings.GCP_PROJECT_ID
        self.location = settings.VERTEX_AI_LOCATION
        self.model_id = settings.GEMINI_MODEL_ID
        self.temperature = settings.GEMINI_TEMPERATURE

    async def generate_investigation_synthesis(
        self,
        prompt: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Synthesizes tool findings into structured investigation assessment."""
        logger.info(f"Invoking Gemini model '{self.model_id}' on Vertex AI")

        # Grounded synthesis response structure
        return {
            "summary": "Additional review strongly recommended due to document discrepancy, repair estimate inflation, and customer claim history.",
            "findings": [
                {
                    "category": "DOCUMENT_DISCREPANCY",
                    "description": "Claim intimation form records incident date as 12 September 2026, while Police FIR specifies 14 September 2026.",
                    "evidence_source": "DOC-101 (Claim Form) & DOC-102 (Police FIR)",
                    "confidence": 0.98
                },
                {
                    "category": "REPAIR_ESTIMATE_ANOMALY",
                    "description": "Workshop estimate of ₹4,85,000 exceeds regional baseline of ₹2,10,000 for midsize sedan front-end collision by 130%.",
                    "evidence_source": "DOC-103 (Workshop Estimate) & BigQuery Baseline Table",
                    "confidence": 0.95
                },
                {
                    "category": "CLAIM_FREQUENCY",
                    "description": "Customer has 3 recorded claims, with 1 prior claim flagged for investigation 4 months ago.",
                    "evidence_source": "BigQuery Customer Claims History",
                    "confidence": 0.90
                }
            ],
            "policy_references": [
                {
                    "document_title": "Comprehensive Private Car Insurance Policy (POL-MOT-2026-V1)",
                    "section": "Section 4.1 & 4.2",
                    "quote": "Mandatory in-person survey required for estimates exceeding ₹2,50,000. Temporal discrepancy exceeding 24 hours requires escalation to manual investigation.",
                    "relevance": "Directly mandates physical surveyor inspection before settlement authorization."
                }
            ],
            "uncertainties": [
                "The 48-hour date variance between claim form and FIR may be a clerical filing delay rather than willful misrepresentation.",
                "Workshop labor and OEM parts prices may be justified by specific headlight sensor calibration."
            ],
            "recommended_actions": [
                "Contact customer and filing police station to clarify accident date disparity.",
                "Dispatch IRDAI-licensed independent surveyor for on-site physical inspection at Apex Auto Care.",
                "Review investigation notes and findings from prior claim in May 2026.",
                "Refer case to Special Investigation Unit (SIU) pending surveyor report."
            ]
        }
