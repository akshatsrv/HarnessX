# Architecture Decision Records (ADR)

## ADR 001: Modular Monolith vs Microservices for MVP
- **Context:** The team has constrained development hours (2-3 hrs/day) and needs a reliable, testable delivery for the challenge.
- **Decision:** Build a single deployable FastAPI application with strict internal layer boundaries (`domain/`, `services/`, `repositories/`, `integrations/`).
- **Consequences:** Low deployment overhead, single Cloud Run instance, easy local testing, simple transaction boundaries. Can be split into microservices at Stage 3.

## ADR 002: BigQuery for Historical Analytics & Firestore for Operational Cases
- **Context:** Historical claims analysis requires aggregations (average repair costs, frequency counts), while active cases require fast document updates and real-time persistence.
- **Decision:** BigQuery handles analytical queries; Firestore handles mutable case state and analyst notes.
- **Consequences:** Clean separation of analytical vs transactional workloads.

## ADR 003: Deterministic Risk Engine + Gemini Reasoning Agent
- **Context:** Pure LLM scoring can hallucinate, while pure rules lack synthesis and contextual understanding.
- **Decision:** Deterministic rule engine calculates explainable risk points first; Gemini on Vertex AI investigates evidence, queries policies, and structures the findings.
- **Consequences:** High explainability, robust grounding, and verifiable audit trails.
