# Tasks — Implementação de Autenticação e Acesso

Checklist de implementação (ordem sugerida):

## Planejamento e Especificação
- [x] Criar a change e artefatos de planejamento do OpenSpec (`.openspec.yaml`, `proposal.md`, `design.md`, `tasks.md`).

## Backend (XanoScript)
- [x] Criar endpoint PATCH `auth/update_profile_app` em `apis/authentication/3910135_auth_update_profile_app_PATCH.xs`.
- [x] Criar endpoint POST `auth/request_password_reset_app` em `apis/authentication/3910136_auth_request_password_reset_app_POST.xs`.
- [x] Criar endpoint POST `auth/reset_password_app` em `apis/authentication/3910137_auth_reset_password_app_POST.xs`.

## Frontend (Streamlit)
- [x] Modificar `utils.py` para detectar automaticamente respostas com status code `401` ou `403` e limpar o estado da sessão local (auth_token e user_name).
- [x] Implementar a página `pages/Perfil.py` com:
  - Visualização de dados atuais do usuário (consumindo `auth/me_app`).
  - Formulário para editar nome e e-mail (consumindo `auth/update_profile_app`).
  - Fluxo visual e formulário de redefinição de senha com token (consumindo os novos endpoints `auth/request_password_reset_app` e `auth/reset_password_app`).
- [x] Ajustar `app.py` para garantir que o menu da barra lateral e o botão "Sair" permaneçam visíveis e consistentes em todas as navegações.

## Testes e Validação
- [x] Criar um script de teste integrado em `workflow_tests/test_auth_flow.py` (ou em `workflow_tests/` existente) para validar localmente as chamadas de API de login, signup, perfil e redefinição de senha.
- [ ] Executar teste manual no navegador via Streamlit simulando login com credenciais incorretas, expiração de sessão e redefinição de senha.
