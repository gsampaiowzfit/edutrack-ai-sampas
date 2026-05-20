# Design: Endpoints CRUD para `subjects`

## Overview

Implementação RESTful com verificação de propriedade (ownership) usando o `user_id` do usuário autenticado. Todas as queries de leitura e atualização DEVEM filtrar por `user_id`.

## Endpoints

- POST `/subjects`
  - Body: `{ "name": string, "code"?: string, "metadata"?: object }`
  - Behavior: insere `user_id` do contexto autenticado no registro antes de salvar.
  - Response: `201 Created` com o registro criado.

- GET `/subjects`
  - Query params: pagination (`limit`, `offset`) opcional
  - Behavior: retorna apenas records com `user_id = auth.user_id`.
  - Response: `200 OK` com lista paginada.

- GET `/subjects/{id}`
  - Behavior: busca por `id` e `user_id = auth.user_id`. Se não encontrado ou não for do usuário, retornar `404 Not Found`.
  - Response: `200 OK` com o registro.

- PATCH `/subjects/{id}`
  - Body: campos a atualizar
  - Behavior: verificar ownership antes de aplicar atualizações. Se não proprietário, `403 Forbidden` ou `404` (preferência por `404` para não vazar existência).
  - Response: `200 OK` com registro atualizado.

- DELETE `/subjects/{id}`
  - Behavior: verificar ownership; apagar se pertencer; retornar `204 No Content`.

## Implementation details

- Authentication: assumir que `auth.user_id` está disponível no contexto do request (padrão Xano).
- DB access: todas as queries devem incluir `user_id` filter. Para operações por `id`, usar uma query com `id` e `user_id` combinado.
- Validation: usar validação de payload (campos obrigatórios, tamanhos máximos).
- Error handling: retornar erros padronizados JSON `{ "error": "message" }`.

## Tests

- Unit tests para cada endpoint cobrindo:
  - Criação bem-sucedida associada ao `user_id` autenticado.
  - Listagem apenas dos registros do usuário.
  - Acesso negado / `404` ao tentar acessar/alterar/apagar registro de outro usuário.

## Files / Locations

- APIs a criar/atualizar: `apis/subjects/` (um arquivo por endpoint ou `api_group.xs` existente)
- Verificar e reutilizar: `tables/803444_subject.xs`

## Security Notes

- Nunca retornar dados de `subjects` sem filtrar por `user_id`.
- Para endpoints públicos (se existirem), garantir que não exponham `subjects` de usuários ligados.

## Request / Response Examples

- POST /subjects

  Request body:

  {
  "name": "Calculus I",
  "code": "MATH101",
  "description": "Introductory calculus",
  "semester": "2026-1",
  "status": "active"
  }

  Response (201):

  {
  "id": 123,
  "owner_id": 456,
  "name": "Calculus I",
  "code": "MATH101",
  "description": "Introductory calculus",
  "semester": "2026-1",
  "status": "active",
  "created_at": "2026-05-19T12:00:00Z"
  }

- GET /subjects

  Response (200):

  [
  { "id": 123, "owner_id": 456, "name": "Calculus I", "status": "active" },
  { "id": 124, "owner_id": 456, "name": "Physics I", "status": "active" }
  ]

- GET /subjects/{id}

  Response (200):

  {
  "id": 123,
  "owner_id": 456,
  "name": "Calculus I",
  "code": "MATH101",
  "description": "Introductory calculus",
  "semester": "2026-1",
  "status": "active",
  "created_at": "2026-05-19T12:00:00Z"
  }

- PATCH /subjects/{id}

  Request body (partial):

  { "name": "Calculus IA" }

  Response (200): updated subject object

- DELETE /subjects/{id}

  Response (204): no content
