# academic-task-management Specification

## Purpose
TBD - created by archiving change create-academic-tasks-table. Update Purpose after archive.
## Requirements
### Requirement: Create academic task

The system SHALL allow students to create a new academic task for a subject.

#### Scenario: Student creates a task

- **WHEN** student submits task data (title, description, due_date, subject_id)
- **THEN** system stores the task with status "pending" and links it to the authenticated student

#### Scenario: Task validation fails

- **WHEN** student submits task with missing required fields (title or subject_id)
- **THEN** system returns validation error

#### Scenario: Invalid subject reference

- **WHEN** student attempts to create task for non-existent subject
- **THEN** system returns error indicating subject does not exist

### Requirement: Read academic tasks

The system SHALL allow students to view their academic tasks with filtering options.

#### Scenario: Student views all their tasks

- **WHEN** authenticated student requests their tasks
- **THEN** system returns all tasks owned by that student

#### Scenario: Student filters tasks by subject

- **WHEN** student requests tasks for a specific subject
- **THEN** system returns only tasks linked to that subject owned by the student

#### Scenario: Student filters tasks by status

- **WHEN** student requests tasks with status filter (e.g., "pending", "completed")
- **THEN** system returns only tasks matching that status

#### Scenario: Unauthorized access attempt

- **WHEN** student attempts to access another student's tasks
- **THEN** system returns empty result or access denied error

### Requirement: Update academic task

The system SHALL allow students to modify their task details.

#### Scenario: Student updates task details

- **WHEN** student submits updated data (title, description, due_date, status)
- **THEN** system updates the task record

#### Scenario: Student changes task status

- **WHEN** student updates status to valid value (pending, in_progress, completed)
- **THEN** system updates the status

#### Scenario: Invalid status value

- **WHEN** student attempts to set status to invalid value
- **THEN** system returns validation error

### Requirement: Delete academic task

The system SHALL allow students to remove their task records.

#### Scenario: Student deletes a task

- **WHEN** student requests task deletion
- **THEN** system removes the task record from the database

### Requirement: Task data model

The system SHALL store academic tasks with required and optional fields.

#### Scenario: Task schema validation

- **WHEN** task is created or updated
- **THEN** system validates: id (auto), title (required, text), description (optional, text), due_date (required, date), status (required, text), subject_id (required, reference), user_id (required, reference), created_at (auto), updated_at (auto)

