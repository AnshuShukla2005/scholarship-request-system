import json
import os

base_app_dir = r"c:\Users\ANSHU KUMAR\Downloads\Scholarship-Management-ServiceNow\Scholarship-Management-ServiceNow2\github_repo\ServiceNow-Application"

# 1. Business Rules
brs = {
    "validate_student_eligibility.js": """/**
 * Business Rule: Validate Student Eligibility
 * Scope: x_2200409_schola_1
 * Table: x_2200409_schola_1_scholarship_application
 * When: Before Insert/Update
 * Description: Validates income cap and academic percentage thresholds against Program rules.
 */
(function executeRule(current, previous /*null when async*/) {
    if (!current.scholarship_program || current.scholarship_program.nil()) {
        gs.addErrorMessage('Scholarship Program reference is mandatory.');
        current.setAbortAction(true);
        return;
    }

    var progGr = new GlideRecord('x_2200409_schola_1_scholarship_program');
    if (!progGr.get(current.scholarship_program)) {
        gs.addErrorMessage('Selected Scholarship Program is invalid or inaccessible.');
        current.setAbortAction(true);
        return;
    }

    if (progGr.active == false) {
        gs.addErrorMessage('The requested Scholarship Program (' + progGr.program_name + ') is currently inactive.');
        current.setAbortAction(true);
        return;
    }

    var studentGr = new GlideRecord('x_2200409_schola_1_student');
    if (!studentGr.get(current.student)) {
        gs.addErrorMessage('Student profile record could not be resolved.');
        current.setAbortAction(true);
        return;
    }

    // Income Cap Evaluation
    var famIncome = parseFloat(studentGr.annual_family_income || 0);
    var maxAllowed = parseFloat(progGr.maximum_family_income || 0);
    if (maxAllowed > 0 && famIncome > maxAllowed) {
        gs.addErrorMessage('Applicant annual family income (₹' + famIncome.toLocaleString('en-IN') + 
                           ') exceeds maximum permissible income cap of ₹' + maxAllowed.toLocaleString('en-IN') + 
                           ' for ' + progGr.program_name + '.');
        current.setAbortAction(true);
        return;
    }

    // Academic Merit Evaluation
    var acadPerc = parseFloat(studentGr.academic_percentage || 0);
    var minPerc = parseFloat(progGr.minimum_percentage || 0);
    if (minPerc > 0 && acadPerc < minPerc) {
        gs.addErrorMessage('Applicant academic percentage (' + acadPerc + '%) falls below minimum threshold of ' + 
                           minPerc + '% for ' + progGr.program_name + '.');
        current.setAbortAction(true);
        return;
    }
})(current, previous);
""",

    "scholarship_approval_decision_handler.js": """/**
 * Business Rule: Scholarship Approval Decision Handler
 * Scope: x_2200409_schola_1
 * Table: sysapproval_approver
 * When: After Update
 * Description: Synchronizes sysapproval_approver decisions with Scholarship Application record.
 */
(function executeRule(current, previous /*null when async*/) {
    if (current.source_table != 'x_2200409_schola_1_scholarship_application') {
        return;
    }

    var app = new GlideRecord('x_2200409_schola_1_scholarship_application');
    if (app.get(current.sysapproval)) {
        var approverName = current.approver.getDisplayValue() || 'System Approver';
        
        if (current.state == 'approved' && previous.state != 'approved') {
            app.application_status = 'approved';
            app.approved_by = current.approver;
            app.approval_date = new GlideDateTime();
            app.admin_comments = 'Formally approved by ' + approverName + ' on ' + new GlideDateTime().getDisplayValue() + '.';
            app.update();
            gs.info('[SCHOLARSHIP] Application ' + app.application_number + ' marked APPROVED by ' + approverName);
        } else if (current.state == 'rejected' && previous.state != 'rejected') {
            app.application_status = 'rejected';
            app.rejection_reason = current.comments.getJournalEntry(1) || 'Administrative review threshold not met.';
            app.admin_comments = 'Rejected by ' + approverName + ': ' + app.rejection_reason;
            app.update();
            gs.info('[SCHOLARSHIP] Application ' + app.application_number + ' marked REJECTED by ' + approverName);
        }
    }
})(current, previous);
""",

    "generate_disbursement_on_approval.js": """/**
 * Business Rule: Generate Disbursement on Approval
 * Scope: x_2200409_schola_1
 * Table: x_2200409_schola_1_scholarship_application
 * When: After Update
 * Description: Automatically generates financial disbursement schedule and decrements program quota.
 */
(function executeRule(current, previous /*null when async*/) {
    if (current.application_status == 'approved' && previous.application_status != 'approved') {
        var disbGr = new GlideRecord('x_2200409_schola_1_scholarship_disbursement');
        disbGr.initialize();
        disbGr.application = current.sys_id;
        disbGr.student = current.student;
        disbGr.scholarship_program = current.scholarship_program;
        disbGr.amount = current.scholarship_program.amount;
        disbGr.payment_status = 'pending';
        disbGr.insert();
        
        gs.info('[SCHOLARSHIP] Disbursement record generated for Application: ' + current.application_number);

        // Decrement available seat quota
        var progGr = new GlideRecord('x_2200409_schola_1_scholarship_program');
        if (progGr.get(current.scholarship_program) && progGr.available_seats > 0) {
            progGr.available_seats = progGr.available_seats - 1;
            progGr.update();
            gs.info('[SCHOLARSHIP] Program seats decremented for ' + progGr.program_name + '. Remaining: ' + progGr.available_seats);
        }
    }
})(current, previous);
""",

    "document_verification_status_sync.js": """/**
 * Business Rule: Document Verification Status Sync
 * Scope: x_2200409_schola_1
 * Table: x_2200409_schola_1_student_document
 * When: After Insert/Update
 * Description: Checks verification completeness across all mandatory documents for an application.
 */
(function executeRule(current, previous /*null when async*/) {
    if (!current.application || current.application.nil()) return;

    var appGr = new GlideRecord('x_2200409_schola_1_scholarship_application');
    if (!appGr.get(current.application)) return;

    // Only update status if currently under review or documents pending
    if (appGr.application_status == 'draft' || appGr.application_status == 'approved' || appGr.application_status == 'rejected') return;

    var docGr = new GlideRecord('x_2200409_schola_1_student_document');
    docGr.addQuery('application', current.application);
    docGr.query();

    var totalDocs = 0;
    var verifiedDocs = 0;
    var rejectedDocs = 0;

    while (docGr.next()) {
        totalDocs++;
        if (docGr.verification_status == 'verified') verifiedDocs++;
        if (docGr.verification_status == 'rejected') rejectedDocs++;
    }

    if (rejectedDocs > 0) {
        appGr.application_status = 'documents_pending';
        appGr.admin_comments = 'One or more required documents were rejected. Please review feedback in Student Portal.';
        appGr.update();
    } else if (totalDocs > 0 && verifiedDocs === totalDocs) {
        appGr.application_status = 'under_review';
        appGr.admin_comments = 'All mandatory documents verified. Application queued for managerial approval.';
        appGr.update();
    }
})(current, previous);
""",

    "prevent_duplicate_application.js": """/**
 * Business Rule: Prevent Duplicate Application
 * Scope: x_2200409_schola_1
 * Table: x_2200409_schola_1_scholarship_application
 * When: Before Insert
 * Description: Prevents students from submitting multiple active applications to the same program.
 */
(function executeRule(current, previous /*null when async*/) {
    var dupGr = new GlideRecord('x_2200409_schola_1_scholarship_application');
    dupGr.addQuery('student', current.student);
    dupGr.addQuery('scholarship_program', current.scholarship_program);
    dupGr.addQuery('application_status', 'IN', 'submitted,documents_pending,under_review,approved');
    dupGr.query();

    if (dupGr.hasNext()) {
        dupGr.next();
        gs.addErrorMessage('You have already submitted an active application (' + dupGr.application_number + 
                           ') for this scholarship program.');
        current.setAbortAction(true);
    }
})(current, previous);
"""
}

for fname, code in brs.items():
    with open(os.path.join(base_app_dir, "business_rules", fname), "w", encoding="utf-8") as f:
        f.write(code)

# 2. Custom Tables Schema
tables_schema = {
    "x_2200409_schola_1_student": {
        "label": "Scholarship Student",
        "description": "Student master registry storing demographic, academic, and financial baseline data.",
        "fields": [
            {"name": "student_name", "label": "Full Name", "type": "String (100)", "mandatory": True},
            {"name": "roll_number", "label": "Roll / UID Number", "type": "String (40)", "mandatory": True, "unique": True},
            {"name": "email", "label": "Email Address", "type": "Email (100)", "mandatory": True},
            {"name": "department", "label": "Academic Department", "type": "String (80)", "mandatory": True},
            {"name": "academic_percentage", "label": "Academic Score (%)", "type": "Decimal (5,2)", "mandatory": True},
            {"name": "annual_family_income", "label": "Annual Family Income (₹)", "type": "Decimal (12,2)", "mandatory": True},
            {"name": "user_account", "label": "ServiceNow User Account", "type": "Reference (sys_user)", "mandatory": False}
        ]
    },
    "x_2200409_schola_1_scholarship_program": {
        "label": "Scholarship Program",
        "description": "Scholarship catalogs defining eligibility criteria, funding quotas, and timelines.",
        "fields": [
            {"name": "program_name", "label": "Program Title", "type": "String (120)", "mandatory": True},
            {"name": "category", "label": "Eligibility Category", "type": "Choice (merit, need_based, sports)", "mandatory": True},
            {"name": "amount", "label": "Scholarship Amount (₹)", "type": "Decimal (12,2)", "mandatory": True},
            {"name": "minimum_percentage", "label": "Minimum Percentage Cut-off (%)", "type": "Decimal (5,2)", "mandatory": True},
            {"name": "maximum_family_income", "label": "Maximum Income Limit (₹)", "type": "Decimal (12,2)", "mandatory": True},
            {"name": "available_seats", "label": "Seat Quota Allocation", "type": "Integer", "mandatory": True},
            {"name": "active", "label": "Active Status Flag", "type": "Boolean", "mandatory": True}
        ]
    },
    "x_2200409_schola_1_scholarship_application": {
        "label": "Scholarship Application",
        "description": "Core transactional table managing student applications and multi-stage lifecycle states.",
        "fields": [
            {"name": "application_number", "label": "Application ID", "type": "String (40)", "mandatory": True, "unique": True},
            {"name": "student", "label": "Applicant Profile", "type": "Reference (x_2200409_schola_1_student)", "mandatory": True},
            {"name": "scholarship_program", "label": "Scholarship Program", "type": "Reference (x_2200409_schola_1_scholarship_program)", "mandatory": True},
            {"name": "application_status", "label": "Application Lifecycle State", "type": "Choice (draft, submitted, documents_pending, under_review, approved, rejected)", "mandatory": True},
            {"name": "approved_by", "label": "Approving Manager", "type": "Reference (sys_user)", "mandatory": False},
            {"name": "approval_date", "label": "Approval Date & Time", "type": "GlideDateTime", "mandatory": False},
            {"name": "rejection_reason", "label": "Rejection Remarks", "type": "String (500)", "mandatory": False},
            {"name": "admin_comments", "label": "Administrative Tracking Notes", "type": "String (1000)", "mandatory": False}
        ]
    },
    "x_2200409_schola_1_student_document": {
        "label": "Student Document",
        "description": "Evidence records storing identity proofs, marksheets, income certificates, and verification flags.",
        "fields": [
            {"name": "document_name", "label": "Document Descriptor", "type": "String (100)", "mandatory": True},
            {"name": "application", "label": "Parent Application", "type": "Reference (x_2200409_schola_1_scholarship_application)", "mandatory": True},
            {"name": "document_type", "label": "Classification Type", "type": "Choice (income_certificate, marksheet, id_proof, bank_passbook)", "mandatory": True},
            {"name": "verification_status", "label": "Verification State", "type": "Choice (pending, verified, rejected)", "mandatory": True},
            {"name": "verified_by", "label": "Verifying Staff Member", "type": "Reference (sys_user)", "mandatory": False},
            {"name": "rejection_remarks", "label": "Rejection Feedback", "type": "String (500)", "mandatory": False}
        ]
    },
    "x_2200409_schola_1_scholarship_disbursement": {
        "label": "Scholarship Disbursement",
        "description": "Financial ledger storing disbursement tranches, bank transactions, and payment statuses.",
        "fields": [
            {"name": "disbursement_number", "label": "Disbursement ID", "type": "String (40)", "mandatory": True, "unique": True},
            {"name": "application", "label": "Approved Application", "type": "Reference (x_2200409_schola_1_scholarship_application)", "mandatory": True},
            {"name": "student", "label": "Beneficiary Student", "type": "Reference (x_2200409_schola_1_student)", "mandatory": True},
            {"name": "scholarship_program", "label": "Fund Source Program", "type": "Reference (x_2200409_schola_1_scholarship_program)", "mandatory": True},
            {"name": "amount", "label": "Grant Allocation (₹)", "type": "Decimal (12,2)", "mandatory": True},
            {"name": "payment_status", "label": "Disbursement Status", "type": "Choice (pending, processing, completed, failed)", "mandatory": True},
            {"name": "transaction_id", "label": "Bank UTR Reference", "type": "String (80)", "mandatory": False},
            {"name": "disbursement_date", "label": "Disbursement Timestamp", "type": "GlideDateTime", "mandatory": False}
        ]
    }
}

with open(os.path.join(base_app_dir, "tables", "custom_tables_schema.json"), "w", encoding="utf-8") as f:
    json.dump(tables_schema, f, indent=2)

print("Exported custom tables schema and business rules!")
