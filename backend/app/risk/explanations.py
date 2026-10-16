from app.domain.risk import RiskAssessment


class RiskExplanationGenerator:
    """Generates human-readable narrative summarizing why risk signals fired."""

    @staticmethod
    def generate_narrative(assessment: RiskAssessment) -> str:
        if not assessment.signals:
            return "No anomalous risk signals identified. Claim qualifies for standard processing path."

        lines = [f"Claim triggered {len(assessment.signals)} risk indicator(s) resulting in a risk score of {assessment.score}/100 ({assessment.level.value}):"]
        for idx, signal in enumerate(assessment.signals, 1):
            lines.append(f"{idx}. [{signal.severity.value}] {signal.title} (+{signal.points} pts): {signal.description}")

        return "\n".join(lines)
