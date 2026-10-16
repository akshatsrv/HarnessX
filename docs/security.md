# Security, Governance & Human-in-the-Loop Principles

## Core Tenets
1. **Decision Support, Not Decision Maker:** ClaimGuard AI recommends; it never autonomously denies claims or initiates financial disbursements.
2. **Least Privilege IAM:** Cloud Run service accounts hold narrow IAM roles (e.g., `roles/bigquery.dataViewer`, `roles/aiplatform.user`, `roles/datastore.user`).
3. **Data Minimization:** Prototype uses strictly synthetic customer and vehicle data. No PII is logged or transmitted.
4. **Untrusted Input Sanitation:** Uploaded documents are treated as untrusted data inputs, never as system instructions.
5. **Signed URLs:** Direct Cloud Storage uploads utilize short-lived time-bounded signed URLs.
6. **Auditability:** Every case note, status change, and tool execution is timestamped with analyst ID and version metadata.
