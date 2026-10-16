# Demo Video Script (3-4 Minutes)

## 0:00 - 0:25 | The Problem: Manual Claims Overload
- Hook: In modern insurance, fraud and misstatement investigation takes days of manual cross-referencing between repair bills, police reports, and complex policy terms.
- Show traditional analyst workflow: multiple open tabs, conflicting dates, lost in policy PDFs.

## 0:25 - 0:50 | Introducing ClaimGuard AI
- ClaimGuard AI combines Document AI, BigQuery historical benchmarks, and Gemini on Vertex AI into a single human-in-the-loop dashboard.
- Introduce Claim `CLM-10291` (Honda City, ₹4,85,000 claim).

## 0:50 - 1:20 | Claim Intake & Document Intelligence
- Open Claim `CLM-10291`.
- View uploaded documents: `claim_form.pdf`, `police_report.pdf`, `repair_estimate.pdf`.
- Show extracted fields and automatic detection of **date mismatch** (12 Sept vs 14 Sept).

## 1:20 - 1:50 | Explainable Risk Assessment
- Display the deterministic risk score: **90/100 (HIGH RISK)**.
- Break down the explicit signals:
  - Document Date Mismatch (+15)
  - Repair Estimate Anomaly (+20)
  - Prior Claims in Past 6 Months (+20)
  - High Claim Amount (+15)

## 1:50 - 2:50 | Gemini AI Investigation & Policy Retrieval
- Click **"Investigate with AI"**.
- Watch real-time tool execution timeline:
  - ✓ Historical claims queried from BigQuery
  - ✓ Repair estimate baseline verified (₹2,10,000 vs ₹4,85,000)
  - ✓ Relevant policy retrieved from Vertex AI Search
- Review the generated structured investigation report, policy citation, and recommended human actions.

## 2:50 - 3:20 | Case Creation & Persistent Record
- Click **"Create Investigation Case"**.
- Add analyst review note.
- Refresh page to demonstrate Firestore persistence.

## 3:20 - 4:00 | Cloud Architecture & Conclusion
- Review the Google Cloud architecture diagram (Cloud Run, Vertex AI, BigQuery, Firestore, Document AI).
- Closing statement: ClaimGuard AI empowers analysts to make faster, fairer, and fully auditable decisions.
