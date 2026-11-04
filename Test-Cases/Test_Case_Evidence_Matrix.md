# Scholarship Request System — Test Case Evidence Matrix

**ServiceNow Instance:** `https://dev437906.service-now.com`  
**Application Scope:** `x_2200409_schola_1`  
**Test Suite Script:** `scratch/run_full_phase5_test_suite.js`  
**Execution Timestamp:** November 02, 2026  
**Final Status:** 15 / 15 PASSED (100% Success Rate)

---

| Test ID | Test Scenario | Preconditions | Execution Steps | Expected Outcome | Actual Empirical Result | Status | Evidence Artifact |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: | :--- |
| **TC-01** | Student Registration & Validation | Scoped table `student` active | Insert record with student name, valid email, CGPA, and annual income | Record inserted; returns unique 32-char `sys_id` | Record inserted successfully (`e13552b5...`) | **PASS** | `fig03_student_records.png` |
| **TC-02** | Program Creation & Quota Setting | Scoped table `scholarship_program` active | Insert program with 5 seats, 70% min score, $50,000 grant | Record inserted with specified seats and eligibility rules | Record created with 5 available seats (`ad3552b5...`) | **PASS** | `fig04_program_records.png` |
| **TC-03** | Application Submission Flow | Active student and active program records | Submit application linked to student with 83.1% score | Application created in status `documents_pending` | Created `SCHAPP0001212` in status `documents_pending` | **PASS** | `fig05_applications_list.png` |
| **TC-04** | Ineligible Academic Score Defense | Program with 70% minimum score threshold | Attempt submitting application with 45% score | Business Rule aborts transaction and logs eligibility warning | Insert aborted by BR `Validate Student Eligibility` | **PASS** | `fig08_business_rules.png` |
| **TC-05** | Duplicate Application Prevention | Active application already exists for student | Attempt submitting secondary application for identical scheme | Business Rule detects active submission and aborts insert | Insert aborted by BR `Prevent Duplicate Applications` | **PASS** | `fig08_business_rules.png` |
| **TC-06** | Document Upload & Verification | Application in `documents_pending` status | Upload marksheets and set verification status to `verified` | Application status advances automatically to `under_review` | BR advances status to `under_review` | **PASS** | `fig06_documents_worklist.png` |
| **TC-07** | Manager Approval Workflow | Application in `under_review` with pending approval | Execute approval via `sysapproval_approver` with comments | Application updates to `approved`; triggers child processes | Application updated to `approved` | **PASS** | `fig16_manager_approvals_list.png` |
| **TC-08** | Manager Rejection & Reason Sync | Application in `under_review` with pending approval | Execute rejection with reason "Incomplete academic proof" | Application updates to `rejected`; reason synced to record | Updated to `rejected`; reason synced into record | **PASS** | `fig08_business_rules.png` |
| **TC-09** | Automated Disbursement Generation | Application transitions to `approved` | Inspect `scholarship_disbursement` table for child payout | Automated disbursement created matching program amount | Generated record `DIS0001062` with amount $50,000 | **PASS** | `fig07_disbursements_list.png` |
| **TC-10** | Duplicate Disbursement Blocking | Active disbursement exists for application | Attempt inserting second disbursement for same application | Business Rule aborts insert, enforcing strict 1:1 payout | Insert aborted by BR `Prevent Duplicate Disbursements` | **PASS** | `fig08_business_rules.png` |
| **TC-11** | Seat Quota Automatic Decrement | Program has 5 available seats; 1 grant approved | Query program record after application approval | Available seats decremented by exactly 1 (5 &rarr; 4) | Program seats updated from 5 to 4 | **PASS** | `fig04_program_records.png` |
| **TC-12** | Role-Based Access Control Audit | 45 ACLs registered in `sys_security_acl` | Evaluate roles for Student, Administrator, Manager | Roles strictly separated; zero guest table access | 45 ACLs verified; zero unauthenticated guest leaks | **PASS** | `fig09_security_acls.png` |
| **TC-13** | Multi-Tenant Student Row Isolation | Student session logged into portal | Query application records under student identity | Student only sees own applications; 0 peer records visible | Row-level isolation verified (`current.email == user.email`) | **PASS** | `fig12_student_portal_full.png` |
| **TC-14** | Dashboard & Analytics Data Integrity | 29 scoped platform reports configured | Compare KPI counts against database queries | 100% mathematical consistency across all 8 KPIs & 4 charts | All 8 KPIs & 4 charts match database records exactly | **PASS** | `fig18_executive_dashboard.png` |
| **TC-15** | Smart Event-Driven Notifications | 11 notification templates active | Trigger application lifecycle state changes | Correct recipient routing (`student.email`, `approver`) | All 11 notification templates active & routed | **PASS** | `fig10_notification_templates.png` |
