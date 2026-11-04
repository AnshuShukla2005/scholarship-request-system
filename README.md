# Scholarship Request Management System Using ServiceNow

[![ServiceNow Scope](https://img.shields.io/badge/ServiceNow%20Scope-x__2200409__schola__1-blue.svg)](https://dev437906.service-now.com)
[![Platform Version](https://img.shields.io/badge/Platform-Xanadu%20%2F%20Washington-green.svg)](https://dev437906.service-now.com)
[![License](https://img.shields.io/badge/License-Academic%20Use-lightgrey.svg)](#)
[![Repository Status](https://img.shields.io/badge/Status-Production%20Verified-brightgreen.svg)](https://github.com/AnshuShukla2005/scholarship-request-system)

> **Academic Project Title:** Scholarship Request Management System Using ServiceNow  
> **Student Author:** ANSHU KUMAR (UID: 24BCS10580)  
> **Degree Program:** Bachelor of Engineering in Computer Science & Engineering  
> **Institution:** Department of Computer Science & Engineering, Chandigarh University, Gharuan, Mohali  
> **Project Supervisor:** Assistant Professor, Department of Computer Science & Engineering  
> **Head of Department:** Dr. Sanjeev Kumar, Head of the Department, Department of CSE  
> **ServiceNow Instance:** `https://dev437906.service-now.com`  
> **Scoped Application ID:** `x_2200409_schola_1`

---

## 📌 Project Overview

The **Scholarship Request Management System** is an enterprise-grade cloud application developed on the **ServiceNow** digital workflow platform. It modernizes, streamlines, and secures the end-to-end scholarship management lifecycle in academic institutions. 

By replacing manual paper forms, email chains, and disconnected spreadsheets with a unified system of action, the platform delivers automated eligibility evaluation, multi-stage approval orchestration, document verification worklists, financial disbursement tracking, and real-time executive analytics.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       SCHOLARSHIP REQUEST SYSTEM LIFECYCLE                  │
└─────────────────────────────────────────────────────────────────────────────┘
  1. Portal Discovery ➔ 2. Eligibility Engine ➔ 3. Document Verification
         │                     │                         │
  6. Disbursement       5. Manager Decision    4. Flow Designer Workflow
```

---

## 🎯 Key Objectives

1. **Eliminate Operational Latency**: Reduce scholarship processing turnaround from several weeks to under 48 hours through event-driven workflow automation.
2. **Deterministic Eligibility Enforcement**: Enforce automated academic percentage cut-offs and annual family income caps at the platform level, preventing invalid submissions.
3. **Rigorous Data Isolation & Privacy**: Implement zero-trust Row-Level and Field-Level Access Control Lists (ACLs) ensuring complete privacy of sensitive financial and academic records.
4. **Transparent Applicant Experience**: Provide a modern, self-service Service Portal (`/scholarship`) featuring real-time visual progress timelines, document rejection feedback, and disbursement receipts.
5. **Auditable Financial Accountability**: Automate grant calculation, quota seat decrementing, and audit logging for every financial disbursement tranche.

---

## 🚀 Key Features

- **Responsive Student Portal (`/scholarship`)**: Mobile-friendly self-service catalog, program discovery, dynamic eligibility checker, application progress stepper, and document upload repository.
- **Administrator Operations Center**: Centralized workspace for verification officers with KPI cards, document inspection queues, pending verification worklists, and program quota management.
- **Multi-Stage Approval Workflow**: Flow Designer-driven approval orchestration routing qualified applications to designated Scholarship Approvers with automated timeouts and reminders.
- **Server-Side Business Rules Engine**: Real-time validation preventing duplicate applications, capping income thresholds, and synchronizing document verification states with application lifecycles.
- **Executive Performance Dashboard**: 8 real-time KPI metrics and 4 interactive visual breakdown charts (applications by status, department distribution, fund allocation, and quota exhaustion).
- **Automated Communication Matrix**: 11 event-driven email notification templates keeping students, administrators, and approvers continuously informed.

---

## 🛠️ Technology Stack & Architecture

| Architectural Layer | Implementation Technology | Key Components |
|---|---|---|
| **Cloud Application Platform** | ServiceNow Cloud Platform | Scoped Application Architecture (`x_2200409_schola_1`) |
| **Relational Database** | MariaDB / ServiceNow Database Layer | 5 Custom Tables, Foreign Keys, Referential Integrity |
| **Logic & Business Rules** | Server-Side JavaScript (ES5/ES6) | GlideRecord, GlideAggregate, GlideDateTime, Business Rules |
| **Workflow Automation** | ServiceNow Flow Designer | Multi-Stage Approval Flows, Subflows, Triggers, Actions |
| **User Interfaces** | Service Portal & Next Experience Workspace | AngularJS, HTML5, CSS3/SASS, Bootstrap, REST APIs |
| **Security & RBAC** | Access Control Lists (ACLs) & User Roles | 45 ACL Rules, Contextual Security, Role Hierarchy |
| **Analytics & Reporting** | ServiceNow Performance Analytics & Reports | Single Score KPIs, Bar Charts, Donut Charts, Data Aggregation |

---

## 🗄️ Database Architecture: Five Custom Tables

The application features five interconnected custom tables built within the application scope `x_2200409_schola_1`:

```
┌─────────────────────────────────┐           ┌─────────────────────────────────┐
│          STUDENT TABLE          │           │       SCHOLARSHIP PROGRAM       │
│  (x_2200409_schola_1_student)   │           │(x_2200409_schola_1_scholarship_ │
├─────────────────────────────────┤           │            _program)            │
│ • student_name                  │           ├─────────────────────────────────┤
│ • roll_number (Unique)          │           │ • program_name                  │
│ • email                         │           │ • category (Merit/Need/Sports)  │
│ • department                    │           │ • amount (₹)                    │
│ • academic_percentage           │           │ • minimum_percentage            │
│ • annual_family_income (₹)      │           │ • maximum_family_income (₹)     │
│ • user_account (sys_user ref)   │           │ • available_seats               │
└────────────────┬────────────────┘           └────────────────┬────────────────┘
                 │ 1                                           │ 1
                 │                                             │
                 │              N                              │
                 └──────────────┬──────────────────────────────┘
                                ▼
              ┌───────────────────────────────────┐
              │      SCHOLARSHIP APPLICATION      │
              │(x_2200409_schola_1_scholarship_   │
              │           _application)           │
              ├───────────────────────────────────┤
              │ • application_number (SCHAPP...)  │
              │ • student (Reference)             │
              │ • scholarship_program (Reference) │
              │ • application_status              │
              │ • approved_by / approval_date     │
              │ • rejection_reason                │
              │ • admin_comments                  │
              └─────────┬───────────────────┬─────┘
                        │ 1                 │ 1
                        │                   │
                        ▼ N                 ▼ 1
       ┌────────────────────────┐  ┌──────────────────────────────────┐
       │    STUDENT DOCUMENT    │  │     SCHOLARSHIP DISBURSEMENT     │
       │(x_2200409_schola_1_    │  │(x_2200409_schola_1_scholarship_ │
       │   _student_document)   │  │         _disbursement)           │
       ├────────────────────────┤  ├──────────────────────────────────┤
       │ • document_name        │  │ • disbursement_number (SCHDIS...)│
       │ • application (Ref)    │  │ • application (Ref)              │
       │ • document_type        │  │ • student (Ref)                  │
       │ • verification_status  │  │ • scholarship_program (Ref)      │
       │ • verified_by          │  │ • amount (₹)                     │
       │ • rejection_remarks    │  │ • payment_status                 │
       └────────────────────────┘  │ • transaction_id (Bank UTR)     │
                                   └──────────────────────────────────┘
```

1. **`x_2200409_schola_1_student` (Scholarship Student)**: Master registry storing student personal details, institutional identifiers, academic scores, and family financial baseline.
2. **`x_2200409_schola_1_scholarship_program` (Scholarship Program)**: Program catalog defining grant funding allocations, merit thresholds (`minimum_percentage`), income ceilings (`maximum_family_income`), and quota seats (`available_seats`).
3. **`x_2200409_schola_1_scholarship_application` (Scholarship Application)**: Core transaction record tracking application numbers (`SCHAPP...`), applicant links, program links, and 6-stage lifecycle states (`draft`, `submitted`, `documents_pending`, `under_review`, `approved`, `rejected`).
4. **`x_2200409_schola_1_student_document` (Student Document)**: Evidence repository storing academic transcripts, income certificates, and verification flags with reviewer feedback.
5. **`x_2200409_schola_1_scholarship_disbursement` (Scholarship Disbursement)**: Financial ledger tracking payment releases (`SCHDIS...`), grant amounts, payment statuses, and bank transaction UTR codes.

---

## 👥 User Roles & Access Control

| Role Name | Scoped Role Identifier | Access Level & Responsibilities |
|---|---|---|
| **Scholarship Student** | `x_2200409_schola_1.student` | Self-service portal access. Can browse programs, submit applications, upload documents, and view own records only. Restricted from viewing any other student's data. |
| **Scholarship Administrator** | `x_2200409_schola_1.scholarship_admin` | Full operational control. Can manage student accounts, configure programs, inspect submitted documents, set verification statuses, and monitor operational workspaces. |
| **Scholarship Manager** | `x_2200409_schola_1.scholarship_manager` | Executive approver. Receives formal approval tasks for applications in `under_review` status, authorizes grants, reviews disbursements, and accesses analytics dashboards. |

---

## ⚙️ Server-Side Business Rules

1. **`Validate Student Eligibility`** (*Before Insert/Update*): Validates that applicant's `annual_family_income` does not exceed program's `maximum_family_income`, and that `academic_percentage` meets or exceeds `minimum_percentage`. Aborts submission with user-friendly error messages if criteria are not met.
2. **`Scholarship Approval Decision Handler`** (*After Update on `sysapproval_approver`*): Listens for approval/rejection events on approval records where source table is `scholarship_application`. Updates application status to `approved` or `rejected`, captures approver details, timestamps, and comments.
3. **`Generate Disbursement on Approval`** (*After Update on `scholarship_application`*): Automatically creates financial disbursement record in `pending` status upon approval, links grant amount from program, and decrements available seat quota.
4. **`Document Verification Status Sync`** (*After Insert/Update on `student_document`*): Automatically transitions application to `under_review` once all mandatory documents are marked `verified`, or to `documents_pending` if any document is rejected.
5. **`Prevent Duplicate Application`** (*Before Insert on `scholarship_application`*): Prevents a student from submitting multiple active applications for the same scholarship program.

---

## 📊 Analytics & Reporting

The system features an Executive Performance Dashboard comprising:
- **8 KPI Cards**: Total Applications, Applications Approved, Pending Verification, Pending Manager Approvals, Total Grant Disbursed, Active Programs, Seat Quota Utilization, and Applications Rejected.
- **4 Visual Charts**:
  - *Applications by Lifecycle Status* (Interactive Donut Chart)
  - *Scholarship Applications by Academic Department* (Horizontal Bar Chart)
  - *Fund Distribution Across Categories* (Merit vs Need vs Sports)
  - *Program Quota Utilization & Seat Availability* (Grouped Column Chart)

---

## 📁 Repository Directory Structure

```
scholarship-request-system/
├── README.md                                 # Master Project Documentation & Overview
├── Documentation/                            # Academic Project Documentation & Reports
│   ├── Scholarship_Request_System_Final_Report.pdf   # Complete 41-Page College Academic Report
│   ├── Scholarship_Request_System_Final_Report.docx  # Formatted Word Document
│   ├── Scholarship_Request_System_Final_Report.html  # Standalone Printable Source
│   ├── Table_of_Contents_and_Figure_Index.md        # Complete Section & Figure Mapping
│   └── Screenshot_Gallery.md                        # Catalog of all Visual Evidence
├── ServiceNow-Application/                   # Scoped Application Configurations & Code
│   ├── tables/
│   │   └── custom_tables_schema.json                # Complete 5-table Data Dictionary
│   ├── business_rules/                              # Server-Side JavaScript Implementation
│   │   ├── validate_student_eligibility.js
│   │   ├── scholarship_approval_decision_handler.js
│   │   ├── generate_disbursement_on_approval.js
│   │   ├── document_verification_status_sync.js
│   │   └── prevent_duplicate_application.js
│   ├── security_acls/
│   │   └── security_acls_matrix.md                  # 45 ACL Rules & Row-Level Scripts
│   ├── notifications/
│   │   └── notification_templates.md                # 11 Active Email Notification Rules
│   └── portal_widgets/
│       └── student_portal_widget.md                 # Service Portal Server & Client Scripts
├── Screenshots/                              # 18 Verified High-Resolution PDI Screenshots
│   ├── fig01_scoped_application.png
│   ├── fig02_data_dictionary.png
│   ├── fig03_business_rules.png
│   ├── fig04_access_control_lists.png
│   ├── fig05_notification_templates.png
│   ├── fig06_student_master_list.png
│   ├── fig07_scholarship_programs_list.png
│   ├── fig08_scholarship_applications_list.png
│   ├── fig09_student_documents_worklist.png
│   ├── fig10_disbursements_ledger.png
│   ├── fig11_flow_designer_workflow.png
│   ├── fig12_student_portal_home.png
│   ├── fig13_application_progress_timeline.png
│   ├── fig14_document_verification_feedback.png
│   ├── fig15_disbursement_receipt_details.png
│   ├── fig16_admin_operations_center.png
│   ├── fig17_manager_approval_interface.png
│   ├── fig18_executive_dashboard.png
│   └── github_repository_qr.png                     # Verified High-Resolution QR Code
├── Diagrams/                                 # 8 Architectural & Design Process Diagrams
│   ├── diagram_fig3_1.png                           # 3-Tier ServiceNow Architecture
│   ├── diagram_fig3_2.png                           # Context DFD (Level 0)
│   ├── diagram_fig3_3.png                           # Functional DFD (Level 1)
│   ├── diagram_fig3_4.png                           # Entity Relationship (ER) Schema
│   ├── diagram_fig3_5.png                           # Use Case Model
│   ├── diagram_fig3_6.png                           # Application Lifecycle State Machine
│   ├── diagram_fig3_7.png                           # Multi-Stage Approval Swimlane
│   └── diagram_fig3_8.png                           # Disbursement Sequence Diagram
└── Test-Cases/                               # Automated Test Evidence & Verification
    ├── Test_Case_Evidence_Matrix.md                 # 15/15 Regression Scenarios Passed
    └── Test_Case_Evidence_Matrix.csv                # Tabular Evidence Matrix
```

---

## 🔒 Security, Compliance & Data Isolation Notice

- **Row-Level Isolation**: Under zero-trust ACL architecture, students querying `/scholarship` or table endpoints are evaluated through session-bound context scripts. A student cannot view, modify, or infer another student's applications or documents.
- **Data Privacy & Sanitization**: This repository contains application configurations, schema definitions, business logic, and test evidence. It strictly excludes user passwords, security tokens, personal phone numbers, and live production credentials.
- **Demonstration Data Preservation**: The live ServiceNow Personal Developer Instance (PDI `dev437906`) maintains application approval record `SCHAPP0001176` (Applicant: *Aditya Pending Test*) in `Requested` status for live viva evaluation.

---

## 📱 Quick Verification & Repository Access

Scan the QR code below using any smartphone camera or QR reader to navigate directly to this repository:

<p align="center">
  <img src="Screenshots/github_repository_qr.png" width="220" alt="GitHub Repository QR Code">
  <br>
  <em>https://github.com/AnshuShukla2005/scholarship-request-system</em>
</p>

---

## 📄 License & Academic Attribution

This project is submitted in partial fulfillment of the requirements for the award of the degree of **Bachelor of Engineering in Computer Science & Engineering** at **Chandigarh University, Gharuan, Mohali**.

Copyright © 2026 ANSHU KUMAR (UID: 24BCS10580). All rights reserved.
