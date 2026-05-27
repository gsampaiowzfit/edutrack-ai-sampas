# Design — Autenticação e Acesso

Este documento detalha o design técnico e a arquitetura para implementar os fluxos completos de Autenticação e Acesso no aplicativo EduTrack AI.

## Arquitetura de Endpoints (Backend - XanoScript)

Adicionaremos 3 novos endpoints no grupo de API `Authentication` (em `apis/authentication/`):

### 1. `PATCH auth/update_profile_app`
- **Descrição**: Atualizar o perfil do usuário logado (nome e e-mail).
- **Autenticação**: Requer token de autenticação ativo (`auth = "user"`).
- **Parâmetros de Entrada**:
  - `name` (text, opcional): Novo nome do usuário.
  - `email` (email, opcional): Novo e-mail do usuário.
- **Fluxo lógico**:
  - Validar se o e-mail solicitado é único no banco de dados (caso esteja sendo alterado).
  - Executar um `db.patch user` usando o ID do usuário autenticado (`$auth.id`).
  - Retornar o registro do usuário atualizado.

### 2. `POST auth/request_password_reset_app`
- **Descrição**: Solicitar um token para redefinição de senha.
- **Autenticação**: Público.
- **Parâmetros de Entrada**:
  - `email` (email, obrigatório): E-mail da conta a ser redefinida.
- **Fluxo lógico**:
  - Buscar o usuário pelo e-mail. Caso não exista, retornar erro.
  - Gerar um token de 6 dígitos numéricos.
  - Gravar no campo `password_reset` do usuário:
    - `token`: O token gerado (criptografado via hash de senha pelo Xano).
    - `expiration`: Data atual + 1 hora em milissegundos.
    - `used`: `false`.
  - Retornar o token gerado no JSON de resposta para que o frontend exiba (para fins de simulação e depuração do ambiente).

### 3. `POST auth/reset_password_app`
- **Descrição**: Redefinir a senha do usuário utilizando o token recebido.
- **Autenticação**: Público.
- **Parâmetros de Entrada**:
  - `email` (email, obrigatório).
  - `token` (text, obrigatório).
  - `password` (text, obrigatório): Nova senha do usuário.
- **Fluxo lógico**:
  - Buscar o usuário pelo e-mail.
  - Verificar se o token não foi utilizado e se a expiração é maior que o momento atual.
  - Utilizar `security.check_password` para comparar o token enviado com `$user.password_reset.token`.
  - Atualizar o registro do usuário definindo a nova senha e marcando o token como utilizado (`used: true`).
  - Retornar mensagem de sucesso.

---

## Estrutura do Frontend (Streamlit)

A integração e tratamento da sessão serão implementados de forma uniforme no frontend.

### 1. Persistência de Sessão e Expiração Automática
No arquivo `utils.py`, modificaremos as funções `xano_get`, `xano_post`, `xano_patch` e `xano_delete` para gerenciar a expiração e erros de token:
- Quando a resposta do Xano retornar status code `401` ou `403` (Unauthorized ou Forbidden):
  - Limpar as variáveis de sessão no Streamlit: `st.session_state["auth_token"] = None` e `st.session_state["user_name"] = None`.
  - Disparar um recarregamento da página para forçar o redirecionamento ao Login com uma mensagem explicativa.

### 2. Edição de Perfil e Redefinição de Senha na Interface
No arquivo `pages/Perfil.py`, criaremos uma interface rica e intuitiva que permite ao usuário logado:
- Visualizar seus dados atuais (Nome e E-mail).
- Editar seu perfil através de um formulário que consome `PATCH auth/update_profile_app`.
- Oferecer uma seção para Redefinição de Senha que consome `POST auth/request_password_reset_app` e permite realizar a troca usando o token gerado.

---

## Pseudocódigos do XanoScript

### PATCH `auth/update_profile_app`
```xs
// Update authenticated user's profile
query "auth/update_profile_app" verb=PATCH {
  api_group = "Authentication"
  auth = "user"

  input {
    text? name
    email? email filters=trim|lower
  }

  stack {
    // If updating email, check if it is unique
    if ($input.email != null) {
      db.get user {
        field_name = "email"
        field_value = $input.email
      } as $existing_user

      if ($existing_user != null) {
        precondition ($existing_user.id == $auth.id) {
          error_type = "accessdenied"
          error = "This email is already in use by another user."
        }
      }
    }

    db.patch user {
      field_name = "id"
      field_value = $auth.id
      data = {
        name: $input.name
        email: $input.email
      }|filter_empty_text:""
    } as $updated_user
  }

  response = $updated_user
}
```

### POST `auth/request_password_reset_app`
```xs
// Request a password reset token
query "auth/request_password_reset_app" verb=POST {
  api_group = "Authentication"

  input {
    email email filters=trim|lower
  }

  stack {
    db.get user {
      field_name = "email"
      field_value = $input.email
    } as $user

    precondition ($user != null) {
      error_type = "notfound"
      error = "User not found with this email."
    }

    // Generate a 6-digit random token (e.g., 888888 for demo or computed)
    // Here we use a static token or mock for testing
    text $token = "123456"
    timestamp $expiration = "now + 1 hour"

    db.patch user {
      field_name = "id"
      field_value = $user.id
      data = {
        password_reset: {
          token: $token
          expiration: $expiration
          used: false
        }
      }
    }
  }

  response = {
    message: "Reset token generated successfully.",
    token: "123456" // Returned so frontend can simulate e-mail delivery
  }
}
```

### POST `auth/reset_password_app`
```xs
// Reset user's password using the token
query "auth/reset_password_app" verb=POST {
  api_group = "Authentication"

  input {
    email email filters=trim|lower
    text token
    text password
  }

  stack {
    db.get user {
      field_name = "email"
      field_value = $input.email
    } as $user

    precondition ($user != null) {
      error_type = "notfound"
      error = "User not found."
    }

    precondition ($user.password_reset != null) {
      error_type = "accessdenied"
      error = "No password reset requested for this user."
    }

    precondition ($user.password_reset.used == false) {
      error_type = "accessdenied"
      error = "This token has already been used."
    }

    // Compare stored password reset expiration with now
    timestamp $now = "now"
    precondition ($user.password_reset.expiration > $now) {
      error_type = "accessdenied"
      error = "This token has expired."
    }

    // Verify token matches (since password_reset.token is a password type)
    security.check_password {
      text_password = $input.token
      hash_password = $user.password_reset.token
    } as $token_ok

    precondition ($token_ok) {
      error_type = "accessdenied"
      error = "Invalid reset token."
    }

    // Update password and mark token as used
    db.patch user {
      field_name = "id"
      field_value = $user.id
      data = {
        password: $input.password
        password_reset: {
          used: true
        }
      }
    }
  }

  response = {
    message: "Password reset successfully. You can now login with your new credentials."
  }
}
```
