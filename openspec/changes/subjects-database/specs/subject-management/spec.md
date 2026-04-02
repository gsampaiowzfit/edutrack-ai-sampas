## ADDED Requirements

### Requirement: Subject records are owned by the creating user

Each subject record SHALL include an owner reference that links the subject to the authenticated user who created it.

#### Scenario: Create subject with ownership

- **WHEN** an authenticated user creates a new subject record
- **THEN** the subject is saved with the user's ID as its owner

### Requirement: Users can create academic subjects

The system SHALL allow authenticated users to create subjects with at least a name and owner reference.

#### Scenario: Successful subject creation

- **WHEN** a logged-in user submits a valid subject payload
- **THEN** the system creates the subject and returns the created record

### Requirement: Users can list only their own subjects

The system SHALL return only subjects owned by the authenticated user when listing subjects.

#### Scenario: List subjects for current user

- **WHEN** a user requests their subject list
- **THEN** the response contains only subjects where owner equals the requesting user's ID

### Requirement: Users can update owned subjects only

The system SHALL allow authenticated users to modify subject records only if they are the owner.

#### Scenario: Update owned subject

- **WHEN** the owner of a subject updates the subject data
- **THEN** the update succeeds and the subject is changed

#### Scenario: Prevent update of another user's subject

- **WHEN** a user attempts to update a subject they do not own
- **THEN** the system rejects the request with an access control error

### Requirement: Users can delete owned subjects only

The system SHALL allow authenticated users to delete subject records only if they are the owner.

#### Scenario: Delete owned subject

- **WHEN** the owner of a subject requests deletion
- **THEN** the subject is removed from the database

#### Scenario: Prevent deletion of another user's subject

- **WHEN** a user requests deletion of a subject they do not own
- **THEN** the system rejects the request with an access control error

### Requirement: Subject records support automated discipline data

Each subject record SHALL include fields that support future automation and organization, such as optional code, description, semester, and status.

#### Scenario: Create subject with metadata

- **WHEN** a user creates a subject with metadata fields
- **THEN** the subject record stores those fields for future automation use
