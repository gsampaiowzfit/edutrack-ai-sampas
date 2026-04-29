## Why

Professors need a way to evaluate student performance by assigning grades to specific academic activities. Currently, there is no mechanism to record grades for activities, making it difficult to track student progress and generate reports. This change enables grade recording for activities, supporting the academic management workflow.

## What Changes

- Add a new table to store activity grades linked to students and activities.
- Create API endpoints for professors to submit and manage grades.
- Implement ownership and permission controls ensuring only authorized users can access grades.
- Establish the foundation for future features like grade history and analytics.

## Capabilities

### New Capabilities

- `activity-grades`: Manage grades for academic activities, including create/read/update/delete operations and permission-based access control.

### Modified Capabilities

- (none)

## Impact

- New database table for activity grades in Xano.
- New API endpoints for grade CRUD operations.
- Integration with existing user authentication system.
- Potential extension of existing subject and task structures.