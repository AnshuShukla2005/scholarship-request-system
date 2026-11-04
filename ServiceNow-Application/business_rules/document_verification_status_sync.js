/**
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
