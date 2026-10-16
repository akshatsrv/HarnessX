# ClaimGuard AI

## Product Requirements, MVP Delivery Plan, and Enterprise Scale-Up Blueprint

**Project type:** AI-powered insurance claims investigation and
fraud-risk decision support\
**Challenge area:** Banking, Financial Services and Insurance (BFSI)\
**Primary cloud:** Google Cloud\
**MVP target:** Working, publicly accessible prototype\
**Development constraint:** Approximately 2--3 hours per person per day\
**Architecture strategy:** Modular monolith first; evolve to
event-driven services when justified

------------------------------------------------------------------------

# 1. Executive Summary

**ClaimGuard AI** is an AI-powered insurance claims investigation
platform that helps claims analysts review potentially suspicious claims
faster and more consistently.

It combines claim-document extraction, explainable risk indicators,
historical claim analytics, insurance-policy retrieval, and
Gemini-powered investigation into one workflow.

The system does not simply return a fraud score. It helps an analyst
understand:

-   What information was found in submitted documents?
-   Which risk indicators were triggered?
-   What historical claim information is relevant?
-   Which policy or procedure applies?
-   What evidence supports the assessment?
-   What should the analyst do next?

The MVP will use synthetic claims and fictional customer data. It will
demonstrate an end-to-end workflow without connecting to a real
insurer's systems or making autonomous claim-denial decisions.

**Core workflow:** **Ingest → Extract → Assess → Investigate → Explain →
Recommend → Record**

## Product positioning

Traditional fraud detection asks:

> Is this claim suspicious?

ClaimGuard AI asks:

> Why does this claim need attention, what evidence supports that
> assessment, which policy applies, and what should the investigator do
> next?

------------------------------------------------------------------------

# 2. Problem Statement

Insurance companies process many claims that require information to be
gathered from different sources, including claim forms, police or
incident reports, repair estimates, insurance policy documents, customer
and vehicle history, previous claims, and investigation guidelines.

Investigators often review these sources manually, reconcile conflicting
information, compare claims against historical patterns, and decide
whether further investigation is necessary.

This creates several challenges:

1.  **Manual effort:** Evidence is spread across documents, databases
    and policy repositories.
2.  **Slow investigation:** Analysts spend time gathering information
    before assessing a claim.
3.  **Inconsistent assessments:** Similar evidence may be interpreted
    differently.
4.  **Limited explainability:** A risk score alone does not show which
    facts caused a claim to be flagged.
5.  **Missed relationships:** Repeated patterns or unusual estimates can
    be difficult to spot manually.
6.  **Policy uncertainty:** Relevant exclusions, thresholds and
    inspection requirements may be buried in long documents.
7.  **Weak auditability:** Evidence and reasoning may not be recorded
    consistently.

## Problem statement for the pitch deck

> Build an AI-powered insurance claims investigation assistant that
> combines document intelligence, historical claims analytics, policy
> retrieval and explainable AI reasoning to identify claims requiring
> additional review, summarize supporting evidence, and recommend the
> next best action to a human investigator.

------------------------------------------------------------------------

# 3. Proposed Solution

ClaimGuard AI gives a claims analyst one interface for reviewing a claim
and investigating risk signals.

## Main capabilities

### 3.1 Claim intake

-   Select a seeded demo claim or create a new claim.
-   Upload supporting documents.
-   Store documents in Cloud Storage.
-   Track claim processing status.

### 3.2 Document intelligence

-   Extract key fields from supported documents using Document AI.
-   Normalize fields into a common claim data model.
-   Preserve source document and extraction metadata.
-   Identify conflicting values, such as different accident dates.
-   Allow analysts to review extracted fields before relying on them.

### 3.3 Explainable risk assessment

A deterministic risk engine calculates a configurable score using
explicit signals, such as:

-   Claim amount unusually high compared with a relevant baseline
-   Previous claims within a defined period
-   Inconsistency between submitted documents
-   Repair estimate above a comparable baseline
-   Missing required information
-   Policy requirements calling for further inspection

Every score must have a traceable explanation. The prototype's rules and
weights are illustrative, not a statistically validated fraud model.

### 3.4 Historical claims analytics

Use BigQuery to query synthetic historical data, such as:

-   Previous claims for a customer or vehicle
-   Claim frequency
-   Average repair estimate for a comparable damage category
-   Claims with similar attributes
-   Historical investigation outcomes

### 3.5 Policy and procedure retrieval

Use Vertex AI Search / Agent Search to retrieve relevant documents,
including policy coverage, inspection requirements, claims-processing
SOPs, investigation guidelines and escalation procedures.

The agent should reference retrieved policy sections. If a policy cannot
be found, it must say so rather than inventing a rule.

### 3.6 Gemini investigation

Gemini on Vertex AI coordinates the investigation by calling approved
backend tools. It synthesizes the returned evidence into a structured
report containing:

-   Claim summary
-   Risk indicators
-   Evidence and source references
-   Document inconsistencies
-   Relevant policy guidance
-   Uncertainties and missing information
-   Recommended next action

### 3.7 Case management

The analyst can create an investigation case, add notes, and update its
status. Case records are stored in Firestore and persist after a browser
refresh.

### 3.8 Human decision

ClaimGuard AI is a **decision-support system**, not an autonomous fraud
judge.

It can recommend continuing standard processing, requesting documents,
verifying information, arranging an inspection, or sending a claim for
manual investigation. The authorized human investigator remains
responsible for the decision.

------------------------------------------------------------------------

# 4. Example End-to-End Scenario

All names, amounts, policies and events below are fictional
demonstration data.

## 4.1 Submitted claim

  Field                         Example
  ----------------------------- ---------------------------------
  Claim ID                      CLM-10291
  Customer ID                   C10291
  Vehicle                       Honda City
  Accident date in claim form   12 September 2026
  Accident location             Delhi
  Claimed amount                ₹4,85,000
  Damage reported               Front bumper, headlight, bonnet
  Claim status                  Submitted

## 4.2 Supporting documents

The analyst uploads:

1.  `claim_form.pdf`
2.  `police_report.pdf`
3.  `repair_estimate.pdf`
4.  `insurance_policy.pdf`

These documents should be synthetic and contain controlled test facts.

## 4.3 Document extraction results

Document AI extracts the claim identifier, customer and vehicle details,
accident date, incident location, claimed amount, repair line items and
policy identifiers where present.

The system detects that the claim form says **12 September**, while the
police report says **14 September**.

This is a discrepancy requiring verification, not proof of fraud.

## 4.4 Historical analytics

BigQuery returns synthetic historical information:

-   Three previous claims for the customer
-   One earlier claim requiring additional review
-   A historical comparable repair estimate baseline of ₹2,10,000
-   A recent prior claim approximately four months earlier

These values are seeded for the demo. Real comparisons must control for
vehicle model, damage severity, geography, parts, labor rates and other
relevant factors.

## 4.5 Illustrative risk calculation

  Risk signal                     Illustrative points
  ----------------------------- ---------------------
  Previous similar claim                           20
  High claim amount                                15
  Repair estimate anomaly                          20
  Document inconsistency                           15
  Policy inspection condition                      10
  Unusual claim frequency                          10
  **Illustrative total**                   **90/100**

This simple sum demonstrates the interface. Production scoring must
define a maximum, handle duplicate or correlated signals, calibrate
thresholds, and validate outcomes against representative labeled data.
The implementation must display its actual computed result, not hardcode
this example.

## 4.6 Gemini investigation report

**Assessment:** Additional investigation recommended

**Key findings:**

1.  The claimed amount is above the seeded historical comparable
    baseline.
2.  A prior claim exists in the synthetic customer history.
3.  The accident dates differ across two documents.
4.  A retrieved policy section requires additional inspection for the
    relevant claim category.

**Uncertainties:**

-   The date discrepancy may have a legitimate explanation.
-   The historical estimate is a comparison baseline, not a definitive
    repair valuation.
-   Previous claims are not proof of wrongdoing.

**Recommended next steps:**

1.  Verify the accident date with the customer or source documents.
2.  Validate the repair estimate.
3.  Review the prior claim.
4.  Arrange an inspection if the applicable policy requires it.
5.  Refer the case to an authorized investigator.

**Final disposition:** Pending human review.

## 4.7 Case creation

After reviewing the report, the analyst selects **Create Investigation
Case**.

The system saves the case ID, claim ID, risk score and signals,
investigation report, policy references, recommended next steps, analyst
ID, status, and timestamps.

The dashboard displays the case as `UNDER_INVESTIGATION`.

------------------------------------------------------------------------

# 5. MVP User Experience

The MVP needs four core screens.

## Screen 1 --- Claims dashboard

Display total demo claims, claims requiring review, open investigation
cases, recent claims, risk level and status.

Metrics must be calculated from demo data or clearly labeled as sample
metrics. Do not present fabricated savings or fraud-prevention results
as real outcomes.

## Screen 2 --- Claim details

Display claim and customer identifiers, claimed amount, incident
details, uploaded documents, extracted fields, document discrepancies,
risk score and individual risk signals.

Primary action: **Investigate with AI**.

## Screen 3 --- AI investigation

Show an investigation timeline whose steps reflect actual tool
execution:

``` text
✓ Claim details retrieved
✓ Previous claims checked
✓ Repair estimate compared
✓ Documents analyzed
✓ Policy guidance retrieved
✓ Investigation report generated
```

The report displays summary, evidence, sources, risk factors, missing
information and recommended action.

## Screen 4 --- Investigation case

Display case ID, linked claim, investigation summary, evidence
references, analyst notes, status and timestamps.

Example statuses:
`OPEN → UNDER_INVESTIGATION → PENDING_INFORMATION → CLOSED`.

Closing a case does not imply that a claim was legally or financially
adjudicated.

------------------------------------------------------------------------

# 6. Functional Scope

## 6.1 Must-have MVP

-   [ ] Firebase Authentication
-   [ ] Claims dashboard with synthetic data
-   [ ] Claim details screen
-   [ ] Document upload to Cloud Storage
-   [ ] Document AI extraction for supported documents
-   [ ] Normalized claim data model
-   [ ] Explainable risk rules
-   [ ] BigQuery historical queries
-   [ ] Gemini investigation using backend tools
-   [ ] Policy retrieval with source references
-   [ ] Structured investigation report
-   [ ] Firestore case creation and status updates
-   [ ] Cloud Run deployment
-   [ ] Firebase Hosting deployment
-   [ ] Public GitHub repository
-   [ ] Working 3--4 minute demo video
-   [ ] Pitch deck using the prescribed template
-   [ ] Basic error handling and reliable seeded demo path

## 6.2 Explicitly out of scope for the MVP

-   Real insurer API integration
-   Real customer or policyholder data
-   Automatic claim approval or denial
-   Sophisticated custom fraud model
-   Graph-based fraud ring detection
-   Complex multi-agent hierarchy
-   Fully real-time event pipeline
-   Kubernetes or GKE
-   Multi-region deployment
-   Enterprise identity integration
-   Automated payments or claim payouts

Reconsider these after the core workflow works and has been evaluated.

------------------------------------------------------------------------

# 7. Technology Stack

## 7.1 Core stack

  -----------------------------------------------------------------------
  Layer                   Technology              Purpose
  ----------------------- ----------------------- -----------------------
  Frontend                React + TypeScript +    Claims dashboard and
                          Vite                    investigation UI

  Frontend hosting        Firebase Hosting        Public web application

  Authentication          Firebase Authentication Analyst sign-in

  API                     Python + FastAPI        REST endpoints and
                                                  orchestration

  API hosting             Cloud Run               Managed application
                                                  deployment

  LLM                     Gemini on Vertex AI     Investigation reasoning
                                                  and report generation

  Document extraction     Document AI             Structured extraction
                                                  from supported
                                                  documents

  Analytical database     BigQuery                Claim history and
                                                  comparison queries

  Operational database    Firestore               Cases, statuses, notes
                                                  and application state

  File storage            Cloud Storage           Uploaded claim
                                                  documents

  Policy retrieval        Vertex AI Search /      Insurance policy and
                          Agent Search            SOP retrieval

  Source control          Git + GitHub            Code, documentation and
                                                  reproducibility

  Testing                 pytest + HTTPX + Ruff   Unit, API and
                                                  code-quality checks
  -----------------------------------------------------------------------

## 7.2 Optional services

  -----------------------------------------------------------------------
  Service                             When to add it
  ----------------------------------- -----------------------------------
  Pub/Sub                             When claims or investigations need
                                      asynchronous event processing

  Vertex AI custom model              When a validated predictive model
                                      adds measurable value

  Cloud SQL / AlloyDB                 When relational transactions, joins
                                      or integrity constraints justify it

  Cloud Build                         When repeatable automated builds
                                      and deployments are needed

  Terraform                           When infrastructure needs
                                      consistent recreation across
                                      environments

  Cloud Monitoring / Trace            As service reliability and
                                      diagnostics needs increase

  ADK / Agent Engine                  When the workflow benefits from
                                      managed agent orchestration and its
                                      operational features
  -----------------------------------------------------------------------

Use the smallest stack that meets the challenge requirements. If a
service is mandatory in the submission rules, include it in a meaningful
working flow rather than mentioning it only in an architecture diagram.

------------------------------------------------------------------------

# 8. System Architecture

## 8.1 MVP architecture

``` text
Analyst Browser
      |
      v
React + TypeScript
Firebase Hosting + Authentication
      |
      v
FastAPI on Cloud Run
      |
      +----------------------+----------------------+
      |                      |                      |
      v                      v                      v
Claim/Risk Services   Investigation Service   Document Service
      |                      |                      |
      v                      v                      v
   BigQuery            Gemini on Vertex AI     Document AI
                             |
                             +---- Approved Tool Functions
                             |           |
                             v           v
                        Policy Search  Claim History

Cloud Storage: original documents
Firestore: case workflow metadata, notes and statuses
```

### Architecture principle

The browser must not call privileged Google Cloud APIs directly. The
backend authorizes access and performs the work. Firebase Authentication
tokens should be validated server-side, and authorization must be
enforced for every protected endpoint.

## 8.2 Enterprise target architecture

``` text
                        Analyst / Partner Apps
                                  |
                       Identity and API Layer
                                  |
                       Claims API on Cloud Run
                                  |
                   +--------------+--------------+
                   |                             |
                   v                             v
            Claim Validation                Operational Store
            and Risk Service                Cloud SQL / Firestore
                   |
                   v
            Pub/Sub Event Topic
                   |
                   v
          Investigation Worker Pool
                   |
            Agent Orchestration
                   |
          +--------+---------+-----------+
          |                  |           |
          v                  v           v
    Document Service   Policy Retrieval  Analytics Tools
          |                  |           |
          v                  v           v
    Cloud Storage      Search Index    BigQuery
          |                  |           |
          +------------------+-----------+
                             |
                             v
                   Investigation Report
                             |
                             v
                  Human Review / Case API

Cross-cutting:
Identity and IAM | Audit | Evaluation | Monitoring | Data Governance
```

This is a target architecture, not a requirement to create all these
services during the prototype.

------------------------------------------------------------------------

# 9. Project Structure Designed for Scale

Start with a **modular monolith**: one deployable backend with clear
internal module boundaries. This minimizes deployment complexity now and
preserves separation for later extraction.

``` text
claimguard-ai/
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── app/
│   │   ├── components/
│   │   ├── features/
│   │   │   ├── claims/
│   │   │   ├── documents/
│   │   │   ├── investigations/
│   │   │   └── cases/
│   │   ├── services/
│   │   ├── types/
│   │   └── main.tsx
│   ├── package.json
│   └── vite.config.ts
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── api/
│   │   │   ├── dependencies.py
│   │   │   └── v1/
│   │   │       ├── health.py
│   │   │       ├── claims.py
│   │   │       ├── documents.py
│   │   │       ├── investigations.py
│   │   │       └── cases.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── logging.py
│   │   │   ├── security.py
│   │   │   └── errors.py
│   │   ├── domain/
│   │   │   ├── claims.py
│   │   │   ├── documents.py
│   │   │   ├── risk.py
│   │   │   ├── investigations.py
│   │   │   └── cases.py
│   │   ├── services/
│   │   │   ├── claim_service.py
│   │   │   ├── document_service.py
│   │   │   ├── risk_service.py
│   │   │   ├── investigation_service.py
│   │   │   └── case_service.py
│   │   ├── risk/
│   │   │   ├── rules.py
│   │   │   ├── scoring.py
│   │   │   └── explanations.py
│   │   ├── agents/
│   │   │   ├── investigator.py
│   │   │   ├── prompts.py
│   │   │   ├── schemas.py
│   │   │   └── tools.py
│   │   ├── retrieval/
│   │   │   ├── policy_search.py
│   │   │   └── citations.py
│   │   ├── repositories/
│   │   │   ├── claims_repository.py
│   │   │   ├── cases_repository.py
│   │   │   └── documents_repository.py
│   │   ├── integrations/
│   │   │   └── google_cloud/
│   │   │       ├── bigquery_client.py
│   │   │       ├── document_ai_client.py
│   │   │       ├── storage_client.py
│   │   │       └── vertex_ai_client.py
│   │   └── schemas/
│   │       ├── requests.py
│   │       └── responses.py
│   ├── tests/
│   │   ├── unit/
│   │   ├── integration/
│   │   └── api/
│   ├── requirements.txt
│   ├── Dockerfile
│   └── pyproject.toml
│
├── data/
│   ├── synthetic/
│   ├── schemas/
│   └── sql/
├── documents/
│   ├── sample-claims/
│   └── sample-policies/
├── infrastructure/
│   ├── terraform/
│   └── firebase/
├── evals/
│   ├── investigation_cases.jsonl
│   ├── expected_signals.jsonl
│   └── README.md
├── docs/
│   ├── problem-statement.md
│   ├── architecture.md
│   ├── api-contracts.md
│   ├── security.md
│   ├── decisions.md
│   ├── demo-script.md
│   └── enterprise-roadmap.md
├── .env.example
├── .gitignore
├── README.md
└── Makefile
```

## Why this structure scales

-   Domain models are independent of Google Cloud SDK objects.
-   Services contain business workflows.
-   Repositories isolate database access.
-   Integrations isolate vendor-specific SDK calls.
-   Agents contain prompts, tool schemas and investigation
    orchestration.
-   API schemas define stable contracts with the frontend.
-   Evaluations preserve test cases for checking investigation quality.
-   Infrastructure is separated from application code.

Do not create empty modules just to match the diagram. Add modules as
their responsibilities are implemented.

------------------------------------------------------------------------

# 10. Core Domain Model

Use stable IDs and explicit schemas from the beginning.

## Claim

``` json
{
  "claim_id": "CLM-10291",
  "customer_id": "C10291",
  "vehicle_id": "V-301",
  "incident_date": "2026-09-12",
  "claimed_amount": 485000,
  "currency": "INR",
  "status": "SUBMITTED",
  "document_ids": ["DOC-001", "DOC-002"],
  "created_at": "2026-10-15T10:00:00Z"
}
```

## Risk assessment

``` json
{
  "assessment_id": "RISK-0001",
  "claim_id": "CLM-10291",
  "score": 82,
  "level": "HIGH",
  "rules_version": "v1",
  "signals": [
    {
      "code": "DOCUMENT_DATE_MISMATCH",
      "severity": "MEDIUM",
      "description": "Dates differ between submitted documents",
      "source_document_ids": ["DOC-001", "DOC-002"]
    }
  ]
}
```

The numeric score is illustrative. The running application must
calculate its actual score.

## Investigation

``` json
{
  "investigation_id": "INV-0001",
  "claim_id": "CLM-10291",
  "status": "COMPLETED",
  "risk_assessment_id": "RISK-0001",
  "summary": "Additional review recommended",
  "findings": [],
  "policy_references": [],
  "recommended_actions": [],
  "model_id": "configured-model-version",
  "prompt_version": "investigation-v1",
  "created_at": "2026-10-15T10:15:00Z"
}
```

## Case

``` json
{
  "case_id": "CASE-10482",
  "claim_id": "CLM-10291",
  "investigation_id": "INV-0001",
  "status": "UNDER_INVESTIGATION",
  "assigned_analyst_id": "ANALYST-001",
  "notes": [],
  "created_at": "2026-10-15T10:20:00Z",
  "updated_at": "2026-10-15T10:20:00Z"
}
```

Store timestamps in UTC and display them in the user's configured
timezone.

------------------------------------------------------------------------

# 11. API Contracts

Use versioned endpoints so future changes do not silently break the
frontend.

  ---------------------------------------------------------------------------------------------
  Method                  Endpoint                                      Purpose
  ----------------------- --------------------------------------------- -----------------------
  GET                     `/api/v1/health`                              Health check

  GET                     `/api/v1/claims`                              List claims

  POST                    `/api/v1/claims`                              Create a claim

  GET                     `/api/v1/claims/{claim_id}`                   Claim details

  POST                    `/api/v1/claims/{claim_id}/documents`         Register/upload a
                                                                        document

  POST                    `/api/v1/documents/{document_id}/extract`     Run extraction

  POST                    `/api/v1/claims/{claim_id}/assess-risk`       Calculate risk

  POST                    `/api/v1/claims/{claim_id}/investigations`    Start investigation

  GET                     `/api/v1/investigations/{investigation_id}`   Read report/status

  POST                    `/api/v1/claims/{claim_id}/cases`             Create a case

  PATCH                   `/api/v1/cases/{case_id}`                     Update case
                                                                        status/notes
  ---------------------------------------------------------------------------------------------

For the MVP, an investigation may run synchronously if latency is
acceptable. If it takes too long, create a job and return an
investigation ID; the frontend can poll for status. Keep the API
contract compatible with this evolution.

------------------------------------------------------------------------

# 12. Investigation Agent Design

Use one orchestrated agent with a bounded tool set for the MVP.

## Approved tools

``` text
get_claim_details(claim_id)
get_customer_claim_history(customer_id)
get_vehicle_claim_history(vehicle_id)
get_repair_estimate_baseline(claim_type, vehicle_type)
get_risk_assessment(claim_id)
search_insurance_policy(query, claim_type)
get_document_extraction(document_id)
create_investigation_case(claim_id, investigation_id)
```

## Investigation sequence

1.  Validate the claim ID and user permissions.
2.  Retrieve the claim and associated documents.
3.  Retrieve the deterministic risk assessment.
4.  Query historical claim information.
5.  Extract document fields if needed.
6.  Search relevant policies and procedures.
7.  Pass evidence to Gemini using a defined input schema.
8.  Validate Gemini's structured output.
9.  Save the investigation report.
10. Let the analyst decide whether to create or update a case.

## Guardrails

-   Gemini may only invoke approved tools.
-   The backend validates all tool arguments and authorization.
-   Do not expose unrestricted SQL execution to the model.
-   Use parameterized queries and controlled query templates.
-   Treat uploaded document text as untrusted data, not instructions.
-   Require source references for policy claims.
-   Separate observed facts from model-generated interpretations.
-   State when evidence is missing or contradictory.
-   Never let the model autonomously reject a claim or initiate a
    payout.
-   Record material analyst actions.

------------------------------------------------------------------------

# 13. Data and Document Plan

## Synthetic data

Create a compact, consistent dataset:

-   500 synthetic customers
-   1,000--3,000 synthetic claims
-   500 synthetic vehicles
-   20--50 policy and procedure documents
-   5--10 carefully prepared demo claims

A larger dataset is unnecessary until query latency and analytical needs
are measured.

## BigQuery tables

``` text
claimguard_demo.claims
claimguard_demo.customers
claimguard_demo.vehicles
claimguard_demo.repair_estimates
claimguard_demo.investigation_outcomes
```

Partition or cluster tables later if real query patterns and data volume
justify it.

## Document AI strategy

Start with documents supported by the selected processor. Verify
document type, region, quotas, pricing and permissions before
integration.

If extraction is unavailable during a demo, provide a clearly labeled
pre-extracted fixture for the seeded sample claim. Do not claim Document
AI ran if the application used fixture data.

## Policy retrieval strategy

Use a small, controlled collection of synthetic policies. Test:

-   A clearly applicable policy
-   Multiple potentially relevant policies
-   A policy exception
-   No matching policy
-   Conflicting or outdated guidance

Record which policy document and section support each recommendation.

------------------------------------------------------------------------

# 14. Environment Setup

## Local tools

-   Python 3.12
-   Node.js 22 LTS
-   Git
-   Google Cloud CLI
-   Firebase CLI
-   Optional Docker Desktop

## Python environment

``` bash
cd backend

python3.12 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
pip install fastapi "uvicorn[standard]" pydantic-settings
pip install google-genai google-cloud-aiplatform
pip install google-cloud-bigquery google-cloud-firestore
pip install google-cloud-storage google-cloud-documentai
pip install pytest httpx ruff

pip freeze > requirements.txt
```

Add ADK if and when the project adopts it for actual agent
orchestration. Keep dependencies pinned and reviewed before production
releases.

## Frontend

``` bash
npm create vite@latest frontend -- --template react-ts
cd frontend
npm install
npm install firebase react-router-dom
npm run dev
```

## Google Cloud authentication

``` bash
gcloud auth login
gcloud auth application-default login
gcloud config set project YOUR_PROJECT_ID
```

Enable the required APIs after selecting the project and confirming
billing:

``` bash
gcloud services enable \
  run.googleapis.com \
  aiplatform.googleapis.com \
  bigquery.googleapis.com \
  firestore.googleapis.com \
  storage.googleapis.com \
  documentai.googleapis.com \
  cloudbuild.googleapis.com \
  artifactregistry.googleapis.com
```

Enable Pub/Sub only when the application begins using it. Configure
Firebase Authentication, Firestore and Hosting in the Firebase console
or CLI. Configure Vertex AI Search separately.

Use local Application Default Credentials for development and dedicated
service accounts for deployed services. Do not commit credentials or
secret files.

------------------------------------------------------------------------

# 15. Development Plan: Approximately 39 Person-Hours

The schedule below is a target, not a guarantee. Cloud permissions,
billing, processor setup and integration issues may require extra time.

  ------------------------------------------------------------------------
  Phase                                        Hours Deliverable
  --------------------- ---------------------------- ---------------------
  Scope, schema and                                3 Approved MVP flow and
  architecture                                       data contracts

  Synthetic data and                               3 Queryable demo claims
  BigQuery                                           

  Document AI                                      4 Extracted fields for
  integration                                        supported sample
                                                     documents

  Risk engine                                      3 Explainable risk
                                                     indicators

  Gemini agent and                                 6 Structured
  tools                                              investigation report

  Policy search and                                3 Evidence-backed
  citations                                          policy retrieval

  Firebase and                                     3 Authentication and
  Firestore                                          persistent cases

  Cloud Run deployment                             3 Deployed backend

  Frontend                                         4 Dashboard and
                                                     investigation screens

  Integration and                                  2 Working end-to-end
  testing                                            flow

  Submission assets                                2 Initial deck, README
                                                     and video preparation

  **Total**                                   **39** **MVP target**
  ------------------------------------------------------------------------

At 2--3 hours per day, 39 person-hours is approximately 13--20
individual workdays for one person. Several people working in parallel
can shorten calendar time, but integration and shared dependencies still
require coordination.

## Milestones

1.  **Data and risk engine:** Claims are queryable and risk indicators
    reproducible.
2.  **Investigation works:** Gemini receives structured evidence and
    produces a validated report.
3.  **Application works locally:** UI triggers investigations and saves
    cases.
4.  **Public deployment works:** Frontend and backend are deployed and
    securely connected.
5.  **Submission ready:** Video, deck, repository and public prototype
    links are tested.

Reserve time for deployment and recording. Do not use all available time
for features.

------------------------------------------------------------------------

# 16. Team Task Distribution

For a team of four, use these ownership areas.

## Developer A --- AI and investigation

-   Gemini integration
-   Tool definitions and validation
-   Investigation prompts and response schema
-   Evidence synthesis and recommendation
-   Evaluation cases

## Developer B --- Data and risk

-   Synthetic data generation
-   BigQuery schema and loading
-   Risk rules and score explanations
-   Historical queries
-   Data fixtures and test scenarios

## Developer C --- Cloud and backend

-   FastAPI structure
-   Firebase authentication verification
-   Firestore repositories
-   Cloud Storage and Document AI
-   Cloud Run deployment and IAM

## Developer D --- Frontend and submission

-   Dashboard and claim details
-   Document upload interface
-   Investigation timeline and evidence view
-   Case management UI
-   README, pitch deck and video

For a two-person team, combine A+B and C+D. For a solo developer,
implement sequentially with the same module boundaries.

## Daily coordination

1.  Identify the single deliverable for each session.
2.  Agree on API and data contracts before parallel work.
3.  Avoid simultaneous edits to shared schemas.
4.  Test integration at the end of the session.
5.  Record blockers and the next action in the project board.

------------------------------------------------------------------------

# 17. Testing and Evaluation

The prototype must demonstrate working functionality, not just a
convincing screen.

## Functional tests

-   Valid claim loads successfully.
-   Unknown claim IDs return a controlled error.
-   Document upload rejects unsupported or oversized files.
-   Extraction results are stored and linked to the correct claim.
-   Risk scoring is deterministic for the same inputs and rules version.
-   Gemini output conforms to the response schema.
-   Policy references point to retrieved source material.
-   Investigation cases persist after refresh.
-   Unauthorized users cannot access protected claims or documents.
-   Failed integrations display useful errors instead of fake success
    messages.

## Investigation quality tests

Prepare 10--20 test cases covering:

-   A normal claim with no notable risk signals
-   A high-value claim with supporting evidence
-   A document-date discrepancy
-   A repeated-claim pattern
-   An unusually high repair estimate
-   Missing documents
-   A relevant policy exception
-   No matching policy
-   Contradictory evidence
-   A case where the right recommendation is to gather more information

Measure whether the system identifies expected signals, cites correct
policies, avoids unsupported claims and recommends an appropriate human
review action.

Do not treat a risk score as a calibrated probability unless it has been
validated as one.

------------------------------------------------------------------------

# 18. Enterprise Scale-Up Roadmap

Build the enterprise path in stages, driven by measurable requirements.

## Stage 1 --- Reliable MVP

-   Modular FastAPI application
-   Versioned API schemas
-   Synthetic test data
-   Structured logs
-   Unit and API tests
-   Firebase Authentication
-   Firestore persistence
-   Cloud Run deployment
-   Evidence-backed investigation reports

## Stage 2 --- Hardened pilot

-   Separate development, staging and production environments
-   Infrastructure as code using Terraform
-   CI/CD with automated tests and controlled promotion
-   Dedicated service accounts and least-privilege IAM
-   Secret management and key rotation
-   Document access controls and retention
-   Structured audit trail
-   Gemini output validation and evaluation
-   Cost, latency and error dashboards
-   Rate limiting, timeouts and bounded retries

## Stage 3 --- Event-driven processing

Introduce Pub/Sub when investigations need asynchronous processing.

``` text
Claim Submitted
      |
      v
Claims API
      |
      v
Pub/Sub Topic
      |
      v
Investigation Worker
      |
      +---- Document Extraction
      +---- Risk Assessment
      +---- Policy Retrieval
      +---- Gemini Investigation
      |
      v
Investigation Result
      |
      v
Firestore / Operational Store
```

Add idempotency keys, retry policies, dead-letter handling, job status
tracking and reconciliation so duplicate events do not create duplicate
investigations.

## Stage 4 --- Scale and specialization

-   Move heavy workloads into independent workers/services only where
    needed.
-   Consider Cloud SQL or AlloyDB for relational consistency
    requirements.
-   Improve BigQuery partitioning and query optimization based on
    observed usage.
-   Add validated ML models where labeled data supports them.
-   Add model and prompt versioning, regression evaluation and fallback
    behavior.
-   Add policy version management and document provenance.
-   Introduce specialist agents only if evaluation shows a clear
    benefit.
-   Define availability, latency and cost SLOs.

## Stage 5 --- Enterprise governance

-   Formal data classification and retention policy
-   Access reviews and audit retention
-   Privacy and regulatory review
-   Human decision controls and appeal/escalation processes
-   Bias and disparate-impact evaluation where appropriate
-   Incident response and disaster recovery
-   Load testing and capacity planning

The enterprise version should not be considered production-ready until
security, legal, privacy, reliability and model-risk reviews are
completed.

------------------------------------------------------------------------

# 19. Enterprise Design Principles From Day One

1.  **Stable contracts:** Keep API request and response schemas explicit
    and versioned.
2.  **Separation of concerns:** Keep business rules separate from LLM
    prompts and cloud SDK clients.
3.  **Traceability:** Every finding should connect to its data or
    document source.
4.  **Reproducibility:** Record the risk-rule version, model identifier
    and prompt version used for each investigation.
5.  **Least privilege:** Give each service only the permissions it
    needs.
6.  **Idempotency:** Design case creation and long-running operations to
    tolerate retries.
7.  **Observability:** Log correlation IDs, timings, errors and tool
    execution metadata without unnecessarily logging sensitive document
    contents.
8.  **Data minimization:** Use synthetic data for the demo and avoid
    unnecessary personal information.
9.  **Human accountability:** Record analyst decisions separately from
    AI recommendations.
10. **Measured evolution:** Split services or add infrastructure only
    when requirements justify the complexity.

------------------------------------------------------------------------

# 20. Submission Deliverables

The challenge requires a deployed, working prototype, an accessible
GitHub repository, a pitch deck using the prescribed template, and a
3--4 minute demonstration video.

## Prototype

-   Public frontend URL
-   Reachable backend/API
-   Working seeded demo claim
-   Document extraction
-   Risk assessment
-   Gemini investigation
-   Policy references
-   Case creation and persistence

## GitHub repository

Include README and setup instructions, architecture diagram, data schema
and synthetic fixtures, source code, `.env.example`, test instructions,
deployment instructions, known limitations and demo flow.

Never commit real credentials or private customer data.

## Pitch deck

Suggested narrative:

1.  Problem
2.  Current investigation gap
3.  ClaimGuard AI solution
4.  End-to-end user journey
5.  Architecture
6.  Google Cloud technology usage
7.  Demo findings and evidence
8.  Business value and measurement plan
9.  Safety, human review and limitations
10. Enterprise roadmap

Use the organizer's exact prescribed template.

## Demo video

Suggested four-minute sequence:

-   **0:00--0:25:** Explain manual claims investigation.
-   **0:25--0:50:** Introduce ClaimGuard AI.
-   **0:50--1:20:** Open a seeded claim and inspect its documents.
-   **1:20--1:50:** Show document extraction and risk indicators.
-   **1:50--2:50:** Trigger Gemini investigation and display
    evidence/policy sources.
-   **2:50--3:20:** Create a case and show persistence.
-   **3:20--3:45:** Explain the Google Cloud architecture.
-   **3:45--4:00:** Summarize the benefit and human-review approach.

Record the actual deployed application. Do not simulate successful
service calls in the recording if they are not working.

------------------------------------------------------------------------

# 21. Definition of Done

-   [ ] Analyst can sign in.
-   [ ] A seeded claim can be opened.
-   [ ] Supporting documents are available.
-   [ ] Document extraction works for the chosen supported format.
-   [ ] Risk indicators are computed and explained.
-   [ ] Historical data is retrieved from BigQuery.
-   [ ] Policy retrieval returns relevant source material.
-   [ ] Gemini generates a structured investigation report.
-   [ ] Recommendations distinguish evidence from uncertainty.
-   [ ] An analyst can create and update a case.
-   [ ] Firestore persists the case.
-   [ ] Frontend and backend are deployed with appropriate access
    controls.
-   [ ] GitHub repository is accessible.
-   [ ] Prescribed pitch deck is complete.
-   [ ] Video is within the required duration.
-   [ ] Demo links are tested from a separate browser/session.
-   [ ] No secrets or real customer data are present in the repository.

------------------------------------------------------------------------

# 22. Final Recommendation

Build **ClaimGuard AI as a modular monolith first**, using React +
TypeScript, FastAPI + Python, Gemini on Vertex AI, Document AI,
BigQuery, Vertex AI Search / Agent Search, Firebase Authentication and
Hosting, Firestore, Cloud Storage, and Cloud Run.

Implement one complete investigation journey using synthetic data. Keep
interfaces and domain models clean, then introduce Pub/Sub, additional
services, stronger governance and specialized models when the product's
measured needs justify them.

**The MVP proves that the workflow works. The enterprise roadmap
explains how to make it secure, reliable, auditable and scalable.**
