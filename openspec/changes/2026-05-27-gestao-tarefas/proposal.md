# academic-task-management Specification

## Purpose

Proporcionar aos alunos a capacidade de gerenciar suas tarefas acadêmicas integrando o backend (XanoScript) e a interface Streamlit. Permite cadastro, listagem agrupada ou ordenada, edição, exclusão, alteração de status e destaque visual de prazos expirados.

## ADDED Requirements

### Requirement: Create academic task

O sistema SHALL permitir que o usuário cadastrado crie uma tarefa vinculada a uma disciplina.

#### Scenario: Usuário cria tarefa com sucesso

- **WHEN** o usuário envia os dados válidos da tarefa (`title`, `description`, `due_date`, `subject_id`)
- **THEN** o sistema SHALL armazenar a tarefa no banco de dados vinculada à disciplina correspondente e ao `user_id` do usuário autenticado, com o status padrão "pending".

#### Scenario: Falha ao criar tarefa por campos ausentes

- **WHEN** o usuário tenta cadastrar uma tarefa sem informar o `title` ou `due_date` ou `subject_id`
- **THEN** o sistema SHALL retornar um erro de validação.

### Requirement: Read academic tasks

O sistema SHALL permitir que o usuário liste todas as suas tarefas de forma agrupada por disciplina ou por prazo, com suporte a filtros de status.

#### Scenario: Usuário lista todas as suas tarefas

- **WHEN** o usuário autenticado solicita a exibição de suas tarefas
- **THEN** o sistema SHALL retornar somente as tarefas criadas pelo próprio usuário (`user_id` correspondente).

#### Scenario: Filtragem por status

- **WHEN** o usuário filtra as tarefas selecionando um status específico ("pending", "in_progress", "completed")
- **THEN** o sistema SHALL retornar apenas as tarefas correspondentes a esse status.

### Requirement: Update academic task

O sistema SHALL permitir que o usuário edite as informações de uma tarefa ou marque-a como concluída.

#### Scenario: Usuário atualiza dados da tarefa

- **WHEN** o usuário atualiza `title`, `description`, `due_date` ou `status` de uma tarefa de sua propriedade
- **THEN** o sistema SHALL salvar as alterações no banco de dados.

#### Scenario: Usuário altera status da tarefa

- **WHEN** o usuário altera o status da tarefa para um valor válido ("pending", "in_progress", "completed")
- **THEN** o sistema SHALL atualizar o status da tarefa no banco de dados.

### Requirement: Delete academic task

O sistema SHALL permitir que o usuário exclua permanentemente uma tarefa.

#### Scenario: Usuário exclui tarefa

- **WHEN** o usuário solicita a exclusão de uma tarefa de sua propriedade
- **THEN** o sistema SHALL remover a tarefa do banco de dados.

### Requirement: Identify overdue tasks

O sistema SHALL calcular e sinalizar se uma tarefa está com o prazo vencido.

#### Scenario: Identificação de prazo vencido

- **WHEN** uma tarefa possui data `due_date` anterior ao dia atual e seu status é diferente de "completed"
- **THEN** o sistema SHALL identificar e sinalizar visualmente a tarefa como vencida.
