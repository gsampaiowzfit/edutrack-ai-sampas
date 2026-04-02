## Why

Students and educators need a way to track academic subjects that belong to each user, with clear ownership and permissions. This change creates a reusable subject database so users can register, manage, and later automate discipline workflows securely.

## What Changes

- Add a dedicated subject management capability for storing academic disciplines.
- Introduce subject ownership linked to the authenticated user who created the record.
- Define access controls so users can only view and manage their own subjects unless shared explicitly later.
- Create the baseline schema and behavior needed for future automation and analytics on subjects.

## Capabilities

### New Capabilities

- `subject-management`: Manage user-owned academic subjects, including create/read/update/delete operations and ownership-based access control.

### Modified Capabilities

- `<existing-name>`: <what requirement is changing>

## Impact

- Database schema changes in the Xano backend.
- New API or function surfaces for subject CRUD operations.
- Existing user auth and account structures may be extended to enforce ownership.
