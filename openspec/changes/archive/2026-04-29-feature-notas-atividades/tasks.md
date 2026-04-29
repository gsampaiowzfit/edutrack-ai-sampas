## 1. Database Setup

- [ ] 1.1 Create activity_grades table in Xano with fields: id, student_id, activity_id, grade_value, graded_by_user_id, created_at, updated_at

## 2. API Implementation

- [ ] 2.1 Create API endpoint POST /activity-grades for professors to submit grades
- [ ] 2.2 Create API endpoint GET /activity-grades to list grades (filtered by ownership)
- [ ] 2.3 Create API endpoint PATCH /activity-grades/{id} to update grades
- [ ] 2.4 Create API endpoint DELETE /activity-grades/{id} to remove grades

## 3. Access Control

- [ ] 3.1 Implement ownership filtering to ensure professors can only access their own students' grades
- [ ] 3.2 Add validation for grade values (e.g., 0-10 scale)