# Tasks — Implementação do endpoint de busca

Checklist de implementação (ordem sugerida):

- [ ] Criar a change e artefatos de planejamento (este change).
- [ ] Criar endpoint `GET /subjects/search` em `apis/subjects/` (ex: `search_GET.xs`).
- [ ] Implementar consulta principal: suportar filtro por `name` (LOWER LIKE) e paginação (`limit`, `offset`).
- [ ] Implementar a computação de `overdue_tasks_count`:
  - Preferir query SQL agregada que conte tarefas atrasadas por `subject_id` para o `user_id` autenticado.
  - Se não for possível, implementar helper Python `scripts/subject_search_helpers.py` com função batch `count_overdue_tasks_for_user(subject_ids, user_id)` e chamá-la a partir do endpoint (evitar N+1).
- [ ] Integrar resultado agregando `overdue_tasks_count` em cada item retornado.
- [ ] Adicionar testes unitários/integrados em `workflow_tests/test_subjects_search.py` cobrindo: busca por nome, filtro overdue, OR lógico, paginação.
- [ ] Atualizar documentação das APIs e páginas relevantes (`pages/Disciplinas.py` ou README).

- [x] Criar a change e artefatos de planejamento (este change).
- [x] Criar endpoint `GET /subjects/search` em `apis/subjects/` (ex: `search_GET.xs`).
- [x] Implementar consulta principal: suportar filtro por `name` (LOWER LIKE) e paginação (`limit`, `offset`).
- [x] Implementar a computação de `overdue_tasks_count`:
  - Preferir query SQL agregada que conte tarefas atrasadas por `subject_id` para o `user_id` autenticado.
  - Se não for possível, implementar helper Python `scripts/subject_search_helpers.py` com função batch `count_overdue_tasks_for_user(subject_ids, user_id)` e chamá-la a partir do endpoint (evitar N+1).
- [x] Integrar resultado agregando `overdue_tasks_count` em cada item retornado.
- [x] Adicionar testes unitários/integrados em `workflow_tests/test_subjects_search.py` cobrindo: busca por nome, filtro overdue, OR lógico, paginação.
- [ ] Atualizar documentação das APIs e páginas relevantes (`pages/Disciplinas.py` ou README).

Notas:

- Garantir que comparações de data usem UTC ou que a timezone seja documentada.
- Validar desempenho com conjuntos grandes (usar índices em `academic_tasks(subject_id, user_id, due_date, completed)`).
