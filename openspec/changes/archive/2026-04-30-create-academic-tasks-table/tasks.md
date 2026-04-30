## 1. Database Setup

- [x] 1.1 Create academic_tasks table in Xano with fields: id, title, description, due_date, status, subject_id, user_id, created_at, updated_at
- [x] 1.2 Set up relationship between academic_tasks and subjects tables via subject_id
- [x] 1.3 Set up relationship between academic_tasks and users tables via user_id

## 2. Access Control and Validation

- [x] 2.1 Implement ownership filtering to ensure students can only access their own tasks
- [x] 2.2 Add validation for required fields (title, subject_id)
- [x] 2.3 Add validation for status values (pending, in_progress, completed)
