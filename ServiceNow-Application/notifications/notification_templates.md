# Notification Templates Configuration Matrix

Scope: `x_2200409_schola_1`  
Total Active Notifications: **11 Notifications**  
Engine: ServiceNow Email Notification & Event Registry

| # | Notification Name | Triggering Event / Condition | Target Recipient | Content Summary |
|---|---|---|---|---|
| **1** | Application Submission Acknowledged | `scholarship_application.inserted` (Status: `submitted`) | Student (`student.email`) | Acknowledges receipt with unique application ID and checklist of required documents. |
| **2** | Document Verification Request | Application moved to `submitted` | Scholarship Approvers group | Alerts verification officers to inspect submitted academic & income certificates. |
| **3** | Document Verified Notification | Document state set to `verified` | Student (`student.email`) | Informs student that submitted evidence has passed formal administrative inspection. |
| **4** | Document Rejection & Resubmission Request | Document state set to `rejected` | Student (`student.email`) | Alerts student of document deficiency with reviewer remarks and direct portal upload link. |
| **5** | Manager Approval Requested | Application moved to `under_review` | Scholarship Approvers group | Dispatches formal approval task with student credentials and program grant amount. |
| **6** | Scholarship Award Approved | Application state set to `approved` | Student (`student.email`) | Official award letter detailing approved grant amount and disbursement schedule. |
| **7** | Application Rejected Notification | Application state set to `rejected` | Student (`student.email`) | Formal communication stating rejection grounds and administrative appeal guidelines. |
| **8** | Financial Disbursement Initiated | Disbursement state set to `pending` | Finance Disbursement Desk | Alerts bursar office to process bank transfer tranche. |
| **9** | Disbursement Credited Confirmation | Disbursement state set to `completed` | Student (`student.email`) | Confirmation of funds transfer containing bank UTR transaction reference. |
| **10** | Quota Depletion Alert | Program `available_seats <= 2` | Scholarship Administrator | Warning to program coordinators that scholarship seats are nearing exhaustion. |
| **11** | Application Inactivity / Reminder | Documents pending > 5 days | Student (`student.email`) | Automated reminder prompting student to complete document submission. |
