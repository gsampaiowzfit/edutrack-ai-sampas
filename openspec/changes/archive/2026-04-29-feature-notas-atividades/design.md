## Context

This change introduces grade recording for academic activities. Currently, the system has users and subjects, but no way to record student grades. The backend uses Xano with XanoScript, and the frontend is Streamlit.

## Goals / Non-Goals

**Goals:**
- Create a database table to store activity grades
- Provide API endpoints for grade CRUD operations
- Implement access control so professors can manage grades for their students

**Non-Goals:**
- Grade history tracking (future enhancement)
- Automated grade calculations or analytics
- Email notifications to students
- Integration with external grade systems

## Decisions

### Database Schema
- **Decision**: Create a new table `activity_grades` with fields for student, activity reference, grade value, and timestamp.
- **Rationale**: Keeps grades separate from activities, allowing flexibility for different activity types.

### API Structure
- **Decision**: Use RESTful endpoints under a new API group `activity-grades`.
- **Rationale**: Follows existing patterns in the project and provides clear separation of concerns.

### Access Control
- **Decision**: Use user_id for ownership filtering; only the professor who created the activity can grade.
- **Rationale**: Leverages existing Xano authentication system.

## Risks / Trade-offs

- **Risk**: Activity reference may change if activities are deleted → **Mitigation**: Use soft delete or require activity existence validation
- **Risk**: Grade validation (e.g., 0-10 scale) not enforced → **Mitigation**: Add validation in API layer
- **Trade-off**: Simplicity vs. flexibility - keeping schema minimal for now to speed up implementation