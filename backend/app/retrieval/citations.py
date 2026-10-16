from typing import List
from app.domain.investigations import PolicyReference


class CitationFormatter:
    """Formats policy references and source document citations for UI presentation."""

    @staticmethod
    def format_citations_markdown(references: List[PolicyReference]) -> str:
        if not references:
            return "No specific policy guidelines required escalation."

        md = ["### Applicable Insurance Policy Sections:"]
        for ref in references:
            md.append(f"- **{ref.document_title}** [{ref.section}]")
            md.append(f"  > \"{ref.quote}\"")
            md.append(f"  *Relevance:* {ref.relevance}\n")
        return "\n".join(md)
