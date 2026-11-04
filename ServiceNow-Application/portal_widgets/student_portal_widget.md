# Service Portal Architecture & Student Portal (`/scholarship`)

Scope: `x_2200409_schola_1`  
Portal URL: `https://dev437906.service-now.com/scholarship`  
Target Persona: Scholarship Student (`x_2200409_schola_1.student`)

## 1. Portal Architecture Overview

The Student Service Portal provides a responsive, mobile-first interface designed to empower scholarship applicants throughout their academic funding lifecycle. Key architectural components include:

- **Program Discovery & Eligibility Matching**: Real-time filtering based on applicant percentage, department, and family income thresholds.
- **Application Progress Timeline**: Five-step visual stepper tracking real-time status transitions (`Draft` → `Submitted` → `Documents Pending` → `Under Review` → `Approved / Rejected`).
- **Document Evidence Vault**: Secure drag-and-drop file upload with immediate verification status badges (`Verified`, `Pending`, `Rejected`).
- **Disbursement Tracker**: Real-time visibility into financial tranches, payment status, and bank UTR transaction numbers.

## 2. Server Script Architecture (Data Isolation)

```javascript
(function() {
    data.userId = gs.getUserID();
    data.student = {};
    data.applications = [];
    data.availablePrograms = [];

    // Resolve Student Profile for Current Logged-In User
    var studentGr = new GlideRecord('x_2200409_schola_1_student');
    studentGr.addQuery('user_account', data.userId);
    studentGr.query();
    if (studentGr.next()) {
        data.student.sys_id = studentGr.getUniqueValue();
        data.student.name = studentGr.getValue('student_name');
        data.student.roll = studentGr.getValue('roll_number');
        data.student.department = studentGr.getValue('department');
        data.student.percentage = parseFloat(studentGr.getValue('academic_percentage'));
        data.student.income = parseFloat(studentGr.getValue('annual_family_income'));

        // Query Applications for This Student Only
        var appGr = new GlideRecord('x_2200409_schola_1_scholarship_application');
        appGr.addQuery('student', data.student.sys_id);
        appGr.orderByDesc('sys_created_on');
        appGr.query();
        while (appGr.next()) {
            data.applications.push({
                sys_id: appGr.getUniqueValue(),
                number: appGr.getValue('application_number'),
                program: appGr.scholarship_program.getDisplayValue(),
                amount: parseFloat(appGr.scholarship_program.amount),
                status: appGr.getValue('application_status'),
                created: appGr.getValue('sys_created_on'),
                comments: appGr.getValue('admin_comments')
            });
        }
    }
})();
```
