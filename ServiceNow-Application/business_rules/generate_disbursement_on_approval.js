/**
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
