# subject-management Specification

## Purpose
Define the database structure and business logic for managing academic subjects in EduTrack AI, including semester association and archiving capabilities.

## Requirements

### Requirement: Create and update subjects
The system SHALL store subject information for each user.

#### Scenario: User creates a new subject
- **WHEN** user creates a new subject with name, teacher, workload, code, and semester
- **THEN** system stores it with user_id association and status "active"

#### Scenario: User updates a subject
- **WHEN** user updates subject details (name, teacher, workload, code, semester)
- **THEN** system saves the updated details

### Requirement: Archive subjects
The system SHALL allow users to archive subjects without deleting them.

#### Scenario: User archives a subject
- **WHEN** user archives an active subject
- **THEN** system updates its status to "archived" and hides it from the default active list

#### Scenario: User unarchives a subject
- **WHEN** user unarchives an archived subject
- **THEN** system updates its status to "active" and restores it to the active list
