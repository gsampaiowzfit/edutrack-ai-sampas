# subjects-search Specification

## Purpose

Planejar e justificar a criação de um endpoint GET `/subjects/search` que permita filtrar disciplinas por nome OU por tarefas atrasadas do usuário autenticado. O objetivo é oferecer pesquisa flexível (substring, case-insensitive) e suporte a filtros por carga de trabalho (tarefas atrasadas), com integração de lógica Python para cálculo de tarefas atrasadas.

## ADDED Requirements

### Requirement: Search subjects by name or overdue tasks

O sistema SHALL expor um endpoint que atenda aos seguintes comportamentos:

- Quando o parâmetro `name` for fornecido: retornar disciplinas cujo `name` contenha a substring (case-insensitive).
- Quando o parâmetro `overdue=true` for fornecido: retornar disciplinas que possuem ao menos uma tarefa atribuída ao usuário autenticado cuja `due_date` seja anterior à data atual e que não esteja marcada como concluída.
- Quando ambos os parâmetros forem fornecidos: aplicar lógica OR — incluir disciplinas que satisfaçam pelo menos uma das condições.
- Resposta paginada: suportar `limit` e `offset`.
- Cada item de resultado deverá incluir: `id`, `name`, `description`, `overdue_tasks_count` (inteiro).

#### Scenario: Busca por nome e/ou tarefas atrasadas

- **WHEN** usuário faz `GET /subjects/search?name=matem&overdue=true` (autenticado)
- **THEN** serviço retorna disciplinas cujo `name` contenha "matem" OU que tenham tarefas atrasadas para o usuário, incluindo `overdue_tasks_count`.

### Conhecimento do Schema

1. Tabela `academic_tasks` contém campos relevantes: `id`, `subject_id`, `user_id` (ou assigned_to), `due_date`, `completed` (boolean).
2. Tabela `subject` (ou `subjects`) contém `id`, `name`, `description`.

## Impact

- Baixa alteração de dados; adiciona endpoint de leitura e lógica de computação de contagem de tarefas atrasadas. Testes automatizados necessários para validação de filtros e paginação.
