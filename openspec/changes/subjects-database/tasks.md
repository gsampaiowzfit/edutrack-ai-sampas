## 1. Data Model

- [ ] 1.1 Create a new `subject` table or equivalent data structure for academic disciplines
- [ ] 1.2 Add owner reference field that links subjects to the authenticated user
- [ ] 1.3 Add metadata fields such as name, code, description, semester, and status

## 2. Access Control

- [ ] 2.1 Implement subject creation with owner assignment from authenticated user context
- [ ] 2.2 Implement listing filtered by current user's owned subjects only
- [ ] 2.3 Implement update and delete operations that verify subject ownership before applying changes

## 3. API / Function Surface

- [ ] 3.1 Add or extend API endpoints / functions for subject CRUD
- [ ] 3.2 Ensure all subject operations require authentication and respect ownership rules

## 4. Validation and Testing

- [ ] 4.1 Add tests for subject creation, listing, update, and deletion by owner
- [ ] 4.2 Add tests that deny access to subjects owned by other users
- [ ] 4.3 Validate required subject fields and ownership enforcement
