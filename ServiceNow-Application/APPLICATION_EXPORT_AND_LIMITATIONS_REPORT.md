# ServiceNow Application Artifacts & Export Limitations Report

**Application:** Scholarship Request System  
**Scope:** `x_2200409_schola_1`  
**Instance:** `https://dev437906.service-now.com`  
**Total Authentic Application XML Artifacts Exported:** **289 Files**  
**Audit Timestamp:** November 04, 2026

---

## 1. Exported & Backed-Up ServiceNow Artifacts (289 XML Files)

The following core application artifacts have been exported directly from ServiceNow in official XML serialization format and committed under both `ServiceNow-Application/update/` and `x_2200409_schola_1/update/` (conforming to native ServiceNow Studio source control standards):

| ServiceNow Metadata Class | Description | Artifact Count | Export Format & Verification |
|---|---|:---:|---|
| **`sys_app`** | Scoped Application Master Record | 1 | Complete application definition (`92550dacc31c931021f03bec05013142`) |
| **`sys_db_object`** | Custom Table Definitions | 5 | All 5 custom tables (`student`, `program`, `application`, `document`, `disbursement`) |
| **`sys_dictionary`** | Table Column & Field Definitions | 66 | Data types, reference qualifiers, mandatory flags, default values |
| **`sys_documentation`** | Field Labels & Help Text | 77 | User-facing labels, plural labels, and hints |
| **`sys_script`** | Server-Side Business Rules | 12 | Eligibility evaluation, approval handlers, disbursement generation |
| **`sys_script_client`** | Client Scripts | 2 | `Populate Student Info onChange`, `Validate Percentage onSubmit` |
| **`sys_ui_policy`** | UI Policies & Dynamic Field Rules | 2 | Conditional field visibility and mandatory locks |
| **`sys_security_acl`** | Access Control Lists (ACLs) | 44 | Row-level and field-level security enforcement rules |
| **`sys_security_acl_role`**| ACL Role Mappings | 47 | Role associations for student, admin, and manager personas |
| **`sys_user_role`** | Scoped Roles | 5 | `student`, `scholarship_admin`, `scholarship_manager`, `user`, `admin` |
| **`sysevent_email_action`** | Email Notification Templates | 11 | Complete email templates, event bindings, and recipient logic |
| **`sys_app_application`** | Application Menus | 1 | Scholarship Request System root navigation menu |
| **`sys_app_module`** | Navigation Modules | 10 | Direct links to list views, workspaces, and portal |
| **`sp_portal`** | Service Portal Definition | 1 | `/scholarship` Portal configuration, theme, and routing |
| **`sp_widget`** | Service Portal Widgets | 1 | Student portal timeline, catalog, and document uploader widget |
| **`sys_ui_page`** | Custom UI Pages | 1 | Administrator Operations Center (`scholarship_admin_workspace`) |
| **`sys_hub_flow`** | Flow Designer Workflows | 1 | `Scholarship Application Approval Workflow` |
| **`pa_dashboards`** | Performance Analytics Dashboards | 1 | `Scholarship Request Dashboard` |
| **`sysauto_script`** | Scheduled Script Executions | 1 | `Check Scholarship Program Expirations` |
| **Total Exported Artifacts** | | **289** | **100% Genuine ServiceNow XML Serialization** |

---

## 2. Unsupported Artifacts & Limitations Report

Per strict architectural standards, ServiceNow Source Control intentionally excludes certain data types and platform tables from application source trees. Below is the transparent audit of unsupported items, reasons for exclusion, and their exact manual export procedures:

### A. Live Database Transactional Records (Excluded by Platform Design)
- **What is Excluded:** Live student applications (e.g., `SCHAPP0001176`, `SCHAPP0001001`), student profile data, physical file attachments (`sys_attachment`), and payment ledger rows.
- **Why Excluded:** ServiceNow Studio source control tracks **application metadata and code**, not business transaction records. Mixing transactional data into Git repositories violates data privacy standards, bloats repository sizes, and causes primary key collisions across instances.
- **How to Export Live Data:**
  1. Navigate to the desired list view: `https://dev437906.service-now.com/x_2200409_schola_1_scholarship_application_list.do`.
  2. Right-click any column header ➔ Select **Export** ➔ Choose **XML (All Records)** or **CSV**.
  3. Save the exported `.xml` file locally as a transaction snapshot.
- **Live Demonstration Record Status:**
  - Application `SCHAPP0001176` (Applicant: *Aditya Pending Test*, Approver: *Scholarship Approvers*) remains live, active, and preserved in **`Requested`** status on `https://dev437906.service-now.com`.

### B. Global Platform User Accounts & Passwords (Security Isolation)
- **What is Excluded:** `sys_user` records, user passwords, hashed credentials, and session tokens.
- **Why Excluded:** `sys_user` is a shared platform table outside the scoped application hierarchy. Exporting user records or credentials to a public or shared Git repository is a severe security vulnerability.
- **Remediation:** Application roles (`x_2200409_schola_1.student`, `x_2200409_schola_1.scholarship_admin`) are fully exported. Upon importing to a new instance, administrators simply assign these roles to users on that instance.

### C. Encrypted Credentials & Authentication Profiles
- **What is Excluded:** `discovery_credentials`, `basic_auth_credentials`, and OAuth secrets.
- **Why Excluded:** ServiceNow encrypts passwords and tokens using two-way encryption keys bound to the specific instance. Encrypted secrets cannot be exported across instances via Git.
- **Remediation:** When linking ServiceNow Studio to GitHub via HTTPS, administrators enter their GitHub Personal Access Token (PAT) directly into ServiceNow's Credential manager (`discovery_credentials`).

### D. System Logs & Audit Trails
- **What is Excluded:** `sys_audit`, `sys_log`, and `sys_history_set` records.
- **Why Excluded:** Instance diagnostic logs and historical transaction deltas are platform telemetry and not part of the deployable application package.

---

## 3. How to Restore or Install This Application on Another Instance

1. **Option A (Via ServiceNow Studio Git Import)**:
   - In ServiceNow, navigate to **System Applications ➔ Studio**.
   - Click **Import From Source Control**.
   - Enter Repository URL: `https://github.com/AnshuShukla2005/scholarship-request-system.git`.
   - Provide GitHub credentials/PAT and select branch `main`.
   - ServiceNow will automatically ingest the 289 XML files in `x_2200409_schola_1/update/` and recreate the entire application with all tables, fields, scripts, ACLs, and workflows.

2. **Option B (Via Retained Update XMLs)**:
   - Navigate to **Retrieved Update Sets ➔ Import Update Set from XML**.
   - Select the desired XML components from `ServiceNow-Application/update/`.
   - Preview and Commit Update Set.
