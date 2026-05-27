# authentication-and-access Specification

## Purpose

Implementar o fluxo completo de autenticação e controle de acesso no EduTrack AI. Isso engloba o cadastro de novos usuários com e-mail e senha, login com credenciais existentes, manutenção segura do estado de autenticação entre páginas, gerenciamento e atualização dos dados do perfil do usuário logado, redefinição de senha através de token, e expiração automática de sessão quando o token expirar no backend do Xano.

## ADDED Requirements

### Requirement: User Registration

The system SHALL allow new users to register an account with a unique email, full name, and password.

#### Scenario: Successful Registration

- **WHEN** user submits name, a unique email, and a valid password (at least 8 characters)
- **THEN** system hashes password, creates a new user in the database, generates an authentication token, and automatically logs in the user

#### Scenario: Registration with Existing Email

- **WHEN** user attempts to register with an email that is already registered
- **THEN** system returns an error indicating that the email is already in use

#### Scenario: Registration with Invalid Data

- **WHEN** user submits registration form with missing fields or a password shorter than 8 characters
- **THEN** system returns validation error and does not create the account

### Requirement: User Authentication (Login)

The system SHALL authenticate existing users with their email and password.

#### Scenario: Successful Login

- **WHEN** user submits valid registered email and correct password
- **THEN** system validates credentials, creates a new authentication token, and logs in the user to the dashboard

#### Scenario: Login with Invalid Credentials

- **WHEN** user submits incorrect email or incorrect password
- **THEN** system returns an invalid credentials error

### Requirement: Session Maintenance and Navigation

 The system SHALL keep the user logged in while they navigate between different pages in the application.

#### Scenario: User navigates between pages

- **WHEN** authenticated user navigates from Dashboard to Disciplinas or Tarefas
- **THEN** system retains session state (auth token and user name) and allows seamless access without requiring re-login

### Requirement: Profile Visualization and Editing

The system SHALL allow authenticated users to view and update their profile details (name and email).

#### Scenario: User views profile

- **WHEN** authenticated user accesses the Profile page
- **THEN** system retrieves and displays user's name and email from the database

#### Scenario: Successful Profile Update

- **WHEN** authenticated user submits updated name and/or email
- **THEN** system updates the user record in the database and updates the active session state

### Requirement: Password Reset Flow

The system SHALL allow users to request a password reset via email and reset their password using a unique token.

#### Scenario: Request Password Reset

- **WHEN** user requests password reset for a registered email
- **THEN** system generates a secure temporary token with a 1-hour expiration, saves it in user's record, and returns success response

#### Scenario: Successful Password Reset

- **WHEN** user submits email, valid non-expired token, and new password
- **THEN** system updates user's password, invalidates the reset token, and allows user to login with new password

#### Scenario: Reset with Expired or Invalid Token

- **WHEN** user attempts password reset with an expired, already used, or incorrect token
- **THEN** system returns validation error

### Requirement: Automatic Token Expiration (Session Timeout)

The system SHALL automatically terminate the user's session when the authentication token expires or becomes invalid.

#### Scenario: Authentication Token Expires

- **WHEN** user attempts to perform an authenticated operation (e.g. load subjects) after the token has expired
- **THEN** system detects the unauthorized response (401/403), clears the local session state (token and name), and redirects user to login screen with a warning message

## Conhecimento do Schema

1. Tabela `user` (ou `user` no singular) já existe no Xano com campos: `id` (int), `created_at` (timestamp), `name` (text), `email` (email), `password` (password), `account_id` (int), `role` (enum), `password_reset` (object com `token`, `expiration`, `used`).
2. Relacionamento: Toda entidade como `subject` e `academic_tasks` deve se relacionar ao usuário por `user_id`.

## Impact

- **Alteração do banco de dados**: Nenhuma (a tabela `user` já possui os campos necessários para autenticação e redefinição de senha).
- **APIs no Backend (XanoScript)**:
  - Criação de novos endpoints em `apis/authentication/`:
    - `PATCH auth/update_profile` ou similar para edição do perfil.
    - `POST auth/request_password_reset` para iniciar redefinição.
    - `POST auth/reset_password` para redefinir a senha com o token.
- **Frontend (Streamlit)**:
  - Criação do arquivo `pages/Perfil.py` com interface para visualização/edição de perfil e solicitação/uso de redefinição de senha.
  - Ajuste de `utils.py` para detectar automaticamente respostas 401/403 e limpar o estado da sessão (implementando a expiração automática de sessão).
  - Garante que a barra lateral e a navegação tratem a sessão de forma integrada.
