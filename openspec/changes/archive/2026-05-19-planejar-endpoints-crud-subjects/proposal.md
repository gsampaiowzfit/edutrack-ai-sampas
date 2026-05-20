# Planejar criação de endpoints CRUD para `subjects`

## Purpose

Planejar a criação de endpoints RESTful (POST, GET, PATCH, DELETE) para a tabela `subjects`, garantindo que cada usuário só consiga acessar e manipular os registros pertencentes a si (controle por `user_id`).

## What Changes

- Criar especificação e tasks para implementar os endpoints CRUD para `subjects`:
  - POST `/subjects` — criar novo subject associado ao `user_id` autenticado
  - GET `/subjects` — listar subjects do usuário autenticado
  - GET `/subjects/{id}` — obter subject se pertencer ao usuário
  - PATCH `/subjects/{id}` — atualizar subject se pertencer ao usuário
  - DELETE `/subjects/{id}` — apagar subject se pertencer ao usuário

- Definir validações de input, respostas HTTP e checagens de propriedade (ownership) em cada endpoint.

## Impact

- Segurança: garante que usuários não consigam ver/editar registros de terceiros.
- Backwards-compatibility: endpoints novos/alterados apenas para `subjects` — impacto isolado.
- Testes: requer testes unitários/integrados para ownership e validações.

## Notes

- Há uma tabela `subjects` no repositório (`tables/803444_subject.xs`). Verificar esquema e reutilizar colunas existentes (garantir campo `user_id`).
- Se houver políticas de autorização centralizadas, integrar as checagens de `user_id` nelas.
