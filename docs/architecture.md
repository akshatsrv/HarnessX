# System Architecture: ClaimGuard AI

## Overview
ClaimGuard AI adopts a **modular monolith** design first, deployed on Google Cloud Run, with clean boundaries to evolve into event-driven microservices when justified.

## MVP Architecture Flow
```text
Analyst Browser
      │
      ▼
React + TypeScript (Firebase Hosting)
Firebase Authentication
      │
      ▼
FastAPI (Cloud Run)
      │
      ├── Claim & Risk Services ───► BigQuery (Historical analytics)
      ├── Document Service ────────► Cloud Storage & Document AI
      └── Investigation Service ───► Gemini on Vertex AI
                                          │
                                          ├── Tools: Policy Search (Vertex AI Search)
                                          ├── Tools: Claim History (BigQuery)
                                          └── Tools: Case Creation (Firestore)
```

## Storage Strategy
- **Cloud Storage:** Original submitted claim documents (PDFs, images).
- **BigQuery:** Synthetic analytical dataset (claims, customer claim history, repair estimate baselines).
- **Firestore:** Operational state, active cases, analyst notes, and investigation reports.
- **Vertex AI Search:** Vector & semantic search over insurance policy documents and investigation guidelines.

## Architectural Principles
1. **Decoupled Business Logic:** Domain models and workflows are independent of Google Cloud SDKs.
2. **Deterministic Risk Pre-Filter:** Rule-based signals run before LLM synthesis to ensure explainability and predictability.
3. **Bounded Tool Execution:** Gemini can only call approved backend tools with strict argument validation.
4. **Zero Client Privileges:** Browser communicates solely via the authorized backend; never calls GCP APIs directly.
