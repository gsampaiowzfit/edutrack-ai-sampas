## Why

Students need a way to track and manage their academic obligations (lessons, tests, assignments) across their subjects. Currently, there is no mechanism to organize and monitor these tasks by discipline, making it difficult for students to stay on top of their academic responsibilities.

## What Changes

- Add a new table to store academic tasks linked to subjects and students.
- Enable students to create, view, update, and delete academic tasks.
- Allow filtering and organizing tasks by subject, status, and due date.
- Establish the foundation for future features like task reminders and grade integration.

## Capabilities

### New Capabilities

- `academic-task-management`: Manage student academic tasks including create/read/update/delete operations with subject linkage, status tracking, and deadline management.

### Modified Capabilities

- (none)

## Impact

- New database table `academic_tasks` in Xano.
- New API endpoints for task CRUD operations.
- Integration with existing `subjects` and `users` tables.
- Frontend updates to display task management interface in Streamlit.
