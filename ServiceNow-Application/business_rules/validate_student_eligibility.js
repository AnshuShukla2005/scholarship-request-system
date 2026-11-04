/**
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
