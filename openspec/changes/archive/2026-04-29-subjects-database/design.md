## Context

The project currently has user and account tables but no dedicated concept for academic subjects. Adding subject management requires a new data model and ownership rules that integrate with authenticated users and existing access control patterns.

## Goals / Non-Goals

**Goals:**

- Define a reusable subject data model with strong ownership semantics
- Enable subject CRUD operations limited to the owning user
- Keep the design extensible for future automation, reporting, and subject sharing
- Avoid broad permission changes until a more explicit sharing model is defined

**Non-Goals:**

- Implement multi-user subject sharing or team-level visibility
- Add advanced scheduling, grading, or curriculum logic in this initial change
- Build a full frontend UI; this change focuses on backend schema and capability

## Decisions

- Use a dedicated `subject-management` capability instead of extending user or account tables.
  - Rationale: isolates discipline data from user metadata and avoids mixing concerns.

- Store ownership as a direct user reference on the subject record.
  - Rationale: ownership is the core access control boundary and should be explicit for all operations.

- Require authenticated user context for all subject operations.
  - Rationale: subjects are personal resources and must not be accessible anonymously.

- Include optional metadata fields such as code, description, semester, and status.
  - Rationale: these fields support later automation and organization without blocking the initial schema.

## Risks / Trade-offs

- Risk: Future sharing or team-level subject access may require schema changes.
  - Mitigation: Keep the initial model simple and owner-focused, then extend with a join table if needed.

- Risk: Duplicate subject names across users may be confusing.
  - Mitigation: Do not enforce global uniqueness; enforce owner-scoped constraints later if needed.

- Risk: Access control may be bypassed if API endpoints do not consistently filter by owner.
  - Mitigation: Design every subject query and mutation around owner checks by default.
