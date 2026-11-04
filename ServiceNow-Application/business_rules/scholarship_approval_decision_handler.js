/**
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
