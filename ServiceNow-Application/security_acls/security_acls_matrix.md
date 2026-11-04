# Role-Based Access Control (RBAC) & ACL Security Architecture

Scope: `x_2200409_schola_1`  
Total Active Access Control Lists (ACLs): **45 Rules**  
Platform Enforcement: Row-Level and Field-Level Security Constraints

## 1. Defined Scoped Roles

| Role Name | Technical Scope Identifier | Description & Access Privilege |
|---|---|---|
| **Scholarship Student** | `x_2200409_schola_1.student` | End-user student privilege. Read/Write access restricted strictly to own profile, applications, and documents. |
| **Scholarship Administrator** | `x_2200409_schola_1.scholarship_admin` | Operational administrator privilege. Full CRUD on Student Master, Programs, Document Verification, and Workspace. |
| **Scholarship Manager** | `x_2200409_schola_1.scholarship_manager` | Executive reviewer privilege. Approver for financial grants, disbursement authorizations, and audit reporting. |

## 2. Table-Level Privilege Matrix

| Custom Table Name | Student Role (`.student`) | Admin Role (`.scholarship_admin`) | Manager Role (`.scholarship_manager`) | Public / Guest |
|---|:---:|:---:|:---:|:---:|
| `x_2200409_schola_1_student` | Read / Update (Self only) | Full CRUD | Read Only | **Blocked** |
| `x_2200409_schola_1_scholarship_program` | Read (Active only) | Full CRUD | Read Only | **Blocked** |
| `x_2200409_schola_1_scholarship_application` | Create / Read (Self only) | Read / Update (All) | Read / Approve / Reject | **Blocked** |
| `x_2200409_schola_1_student_document` | Create / Read (Self only) | Full CRUD / Verify | Read Only | **Blocked** |
| `x_2200409_schola_1_scholarship_disbursement` | Read (Self only) | Create / Read / Update | Read / Approve / Audit | **Blocked** |

## 3. Row-Level Security Script (Student Privacy Isolation)

```javascript
// Applied on x_2200409_schola_1_scholarship_application.read
answer = false;
if (gs.hasRole('x_2200409_schola_1.scholarship_admin') || gs.hasRole('x_2200409_schola_1.scholarship_manager')) {
    answer = true;
} else if (gs.hasRole('x_2200409_schola_1.student')) {
    answer = (current.student.user_account == gs.getUserID());
}
```
