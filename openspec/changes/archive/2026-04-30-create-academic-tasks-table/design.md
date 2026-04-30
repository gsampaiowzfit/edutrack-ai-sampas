## Context

The system currently has users and subjects defined. Students need to track academic tasks (lessons, assignments, tests) for each subject. The backend uses Xano with XanoScript, and the frontend is Streamlit.

## Goals / Non-Goals

**Goals:**

- Create a database table to store academic tasks
- Link tasks to subjects and users
- Support task status tracking and deadline management
- Enable filtering and sorting by subject, status, and due date

**Non-Goals:**

- Automatic reminders or notifications
- Task priority levels (future enhancement)
- Recurring tasks or templates
- Integration with calendar systems

## Decisions

### Table Schema

- **Decision**: Create `academic_tasks` table with fields: id, title, description, due_date, status, subject_id, user_id, created_at, updated_at.
- **Rationale**: Stores all necessary task metadata while maintaining linkage to both subject and user for ownership verification.

### Field Types

- **Decision**: Use `text` for title and description, `date` for due_date, `text` for status (enum-like: "pending", "in_progress", "completed").
- **Rationale**: Text fields are flexible and human-readable; date ensures consistent handling of deadlines.

### Ownership and Access Control

- **Decision**: Filter tasks by user_id to ensure students only see their own tasks.
- **Rationale**: Leverages existing authentication system and prevents cross-user data access.

### Status Enumeration

- **Decision**: Use predefined status values: "pending", "in_progress", "completed".
- **Rationale**: Simplifies validation and filtering without adding complexity of a separate enum table.

## Risks / Trade-offs

- **Risk**: Tasks linked to deleted subjects leave orphaned records → **Mitigation**: Implement soft delete on subjects or require subject validation before task creation
- **Risk**: No audit trail for task modifications → **Mitigation**: Add created_at/updated_at fields; future enhancement could add full audit log
- **Trade-off**: Status as text vs. separate enum table - keeping as text for simplicity now, can refactor later if many status values added
