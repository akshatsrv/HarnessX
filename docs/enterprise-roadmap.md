# Enterprise Scale-Up Roadmap

ClaimGuard AI is architected to scale in five distinct phases:

## Stage 1: Reliable MVP (Current)
- Modular FastAPI monolith on Cloud Run
- Deterministic explainable risk rules
- Grounded Gemini investigation with tool calling
- BigQuery demo dataset & Firestore case persistence
- Firebase Authentication & Hosting

## Stage 2: Hardened Pilot
- Multi-environment staging (Dev, Stage, Prod) via Terraform
- Automated CI/CD pipelines (GitHub Actions & Cloud Build)
- Centralized Secret Manager & automated key rotation
- Granular Document ACLs & Data Retention policies
- Cost and latency monitoring dashboards in Cloud Trace / Cloud Monitoring

## Stage 3: Event-Driven Processing
- Asynchronous ingest & processing via Google Cloud Pub/Sub
- Worker pool on Cloud Run Jobs for batch Document AI OCR & heavy LLM pipelines
- Idempotent processing with dead-letter topics and reconciliation

## Stage 4: Scale & Specialization
- Hybrid analytical/relational storage (Cloud SQL / AlloyDB for transactional consistency)
- Partitioned and clustered BigQuery tables for enterprise-scale claims (millions of records)
- Continuous evaluation pipeline with prompt regression tests

## Stage 5: Enterprise Governance & Compliance
- Full SOC 2 & HIPAA/BFSI compliance auditing
- Bias & disparate-impact evaluation on risk rules
- Automated data redaction for PII / sensitive claim documents
