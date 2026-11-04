/**
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
