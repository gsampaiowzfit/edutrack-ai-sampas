# Design — Endpoint de busca de disciplinas

## Endpoint

- Método: `GET`
- Caminho: `/subjects/search`
- Parâmetros de query:
  - `name` (string, opcional) — substring para busca no nome (case-insensitive).
  - `overdue` (boolean, opcional) — quando `true`, filtra disciplinas com tarefas atrasadas do usuário autenticado.
  - `limit` (int, opcional) — paginação (padrão 20).
  - `offset` (int, opcional) — paginação.

## Resposta (exemplo)

{
"items": [
{"id": 1, "name": "Matemática I", "description": "...", "overdue_tasks_count": 2},
...
],
"total": 123
}

## Implementação proposta

1. Consulta principal (XanoScript / DB):
   - Se `name` presente, buscar subjects com `LOWER(name) LIKE %lower(name)%`.
   - Para `overdue=true`, precisamos calcular se existe pelo menos uma `academic_tasks` associada ao subject e ao usuário autenticado com `due_date < today` e `completed = false`.

2. Abordagem para a lógica de tarefas atrasadas:
   - Opção A (preferida): implementar um helper Python reutilizável (ex: `scripts/subject_search_helpers.py`) com função `count_overdue_tasks_for_user(subject_id, user_id)` que consulta a tabela `academic_tasks` e retorna contagem. O endpoint XanoScript chama esse helper para cada subject retornado ou, preferencialmente, em batch (por exemplo, obter contagens por subject para os subjects retornados) para evitar N+1.
   - Opção B: escrever uma única query SQL agregada que faça LEFT JOIN com `academic_tasks` e conte tasks atrasadas por subject para o `user_id` — isso evita a necessidade de Python, mas pode ficar mais complexo dependendo do engine.

3. Recomendações técnicas:
   - Preferir calcular `overdue_tasks_count` em uma query agregada por subject (mais eficiente) e expor via API. Se o banco ou camada não suportar, implementar função Python que receba lista de `subject_id` e retorne um dict {subject_id: count}.
   - Tratar timezone: usar UTC para comparação de datas no backend ou normalizar `due_date` para UTC antes de comparar com `now()`.
   - Autorização: sempre filtrar por `user_id` do usuário autenticado.

## Pseudocódigo (Python helper)

def count_overdue_tasks_for_user(conn, subject_ids, user_id, today): # conn: conexão ao DB # subject_ids: lista de subject ids # retorna dict {subject_id: count}
sql = """
SELECT subject_id, COUNT(\*) as cnt
FROM academic_tasks
WHERE subject_id IN (:subject_ids)
AND user_id = :user_id
AND completed = false
AND due_date < :today
GROUP BY subject_id
""" # executar e mapear resultados
