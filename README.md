# ClaimGuard AI

AI-Powered Insurance Claims Investigation and Fraud-Risk Decision Support platform designed for Banking, Financial Services, and Insurance (BFSI).

## Overview

ClaimGuard AI combines **Document AI extraction**, **deterministic risk rules**, **BigQuery historical claim analytics**, **Vertex AI Search policy retrieval**, and **Gemini reasoning** into an explainable decision-support workflow for insurance claim analysts.

### Core Workflow
**Ingest → Extract → Assess → Investigate → Explain → Recommend → Record**

---

## Architecture

- **Frontend**: React 18, TypeScript, Vite, Tailwind/Vanilla CSS, hosted on Firebase Hosting
- **Backend**: Python 3.12, FastAPI (Modular Monolith), deployed on Google Cloud Run
- **Authentication**: Firebase Authentication
- **Data & Analytics**: Google Cloud BigQuery (Historical analytics) & Cloud Firestore (Case states)
- **Document Intelligence**: Google Cloud Document AI & Cloud Storage
- **Reasoning Agent**: Gemini on Vertex AI with approved tool functions
- **Policy Retrieval**: Vertex AI Search / Agent Search

---

## Directory Structure

```text
.
├── frontend/                 # React + TypeScript + Vite UI
│   ├── src/
│   │   ├── app/              # Layout and context providers
│   │   ├── components/       # Shared UI components
│   │   ├── features/         # Domain feature screens (claims, documents, investigations, cases)
│   │   ├── services/         # API & Firebase clients
│   │   └── types/            # TypeScript schema types
├── backend/                  # FastAPI Modular Monolith
│   ├── app/
│   │   ├── api/v1/           # Versioned REST endpoints
│   │   ├── core/             # Configuration, logging, security, errors
│   │   ├── domain/           # Core business domain models
│   │   ├── services/         # Application service workflows
│   │   ├── risk/             # Deterministic risk engine & explainability
│   │   ├── agents/           # Gemini investigator agent, prompts & tools
│   │   ├── retrieval/        # Policy search & citation generator
│   │   ├── repositories/     # Storage & persistence abstraction
│   │   ├── integrations/     # Google Cloud SDK clients (BigQuery, DocAI, GCS, Vertex)
│   │   └── schemas/          # Pydantic request/response contracts
│   └── tests/                # Unit, integration, and API tests
├── data/                     # Synthetic data, SQL schemas & BigQuery fixtures
├── documents/                # Sample claims and insurance policy files
├── infrastructure/           # Terraform & Firebase deployment configurations
├── evals/                    # Evaluation benchmark test cases
└── docs/                     # Specifications, architecture, and pitch resources
```

---

## Getting Started

### Prerequisites
- Python 3.12+
- Node.js 22 LTS+
- Google Cloud CLI (`gcloud`)
- Firebase CLI (`firebase-tools`)

### Local Development Setup

1. **Clone & Configure Environment**:
   ```bash
   cp .env.example .env
   ```

2. **Backend Setup**:
   ```bash
   cd backend
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   uvicorn app.main:app --reload --port 8080
   ```

3. **Frontend Setup**:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

4. **Verify Health**:
   Visit `http://localhost:8080/api/v1/health` or view the frontend at `http://localhost:5173`.

---

## Documentation
- [Problem Statement](docs/problem-statement.md)
- [System Architecture](docs/architecture.md)
- [API Contracts](docs/api-contracts.md)
- [Security & Governance](docs/security.md)
- [Enterprise Roadmap](docs/enterprise-roadmap.md)
- [Full Plan & Reference Blueprint](docs/ClaimGuard_AI_Full_Plan_and_Enterprise_Roadmap.md)
