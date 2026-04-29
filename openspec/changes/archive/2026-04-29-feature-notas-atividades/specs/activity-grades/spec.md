# activity-grades Specification

## Purpose

Defines the database structure and API behavior for managing student grades on academic activities.

## ADDED Requirements

### Requirement: Create activity grade
The system SHALL allow professors to create a grade record for a student on a specific activity.

#### Scenario: Professor creates a grade
- **WHEN** professor submits grade data (student_id, activity_id, grade_value)
- **THEN** system stores the grade record with ownership linked to the professor

#### Scenario: Grade validation fails
- **WHEN** professor submits grade with invalid value (negative or above maximum)
- **THEN** system returns validation error

### Requirement: Read activity grades
The system SHALL allow authorized users to view grades for activities they own.

#### Scenario: Professor views their students' grades
- **WHEN** authenticated professor requests grades for their activities
- **THEN** system returns all grades for activities owned by that professor

#### Scenario: Unauthorized access attempt
- **WHEN** user attempts to access grades for activities they don't own
- **THEN** system returns empty result or access denied error

### Requirement: Update activity grade
The system SHALL allow professors to modify existing grade records.

#### Scenario: Professor updates a grade
- **WHEN** professor submits updated grade value for an existing record
- **THEN** system updates the grade record

### Requirement: Delete activity grade
The system SHALL allow professors to remove grade records.

#### Scenario: Professor deletes a grade
- **WHEN** professor requests to delete a grade record
- **THEN** system removes the grade record from the database