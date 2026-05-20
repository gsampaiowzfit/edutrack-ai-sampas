# tasks for "planejar-endpoints-crud-subjects"

- [x] Verify existing `subjects` table schema in `tables/803444_subject.xs` and ensure `user_id` exists. (note: table uses `owner_id`)
- [x] Draft request/response schema examples for each endpoint (POST, GET list, GET single, PATCH, DELETE).
- [x] Implement POST `/subjects` API endpoint under `apis/subjects/` that attaches `auth.user_id` on create. (implemented as `owner_id`)
- [x] Implement GET `/subjects` API endpoint that returns only `subjects` where `user_id = auth.user_id` (add pagination support). (implemented using `owner_id` filter)
- [x] Implement GET `/subjects/{id}` API endpoint with ownership check (`id` + `user_id`).
- [x] Implement PATCH `/subjects/{id}` API endpoint with ownership check and validation. (already implemented)
- [x] Implement DELETE `/subjects/{id}` API endpoint with ownership check. (already implemented)
- [x] Add unit/integration tests covering ownership scenarios and validations. (tests added that statically verify ownership checks)
- [x] Review and document the endpoints in the API group file and update any related frontend usage.

Notes:

- Scope is LIMITED: only implement the CRUD endpoints for `subjects` and ownership checks as requested.
- Do NOT create extra endpoints or unrelated APIs.
