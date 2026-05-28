## Context

O sistema já possui as tabelas `user` e `subject` definidas. Os alunos precisam gerenciar tarefas acadêmicas (lições, trabalhos, provas) associando-as às suas respectivas disciplinas. A tabela `academic_tasks` já está definida no banco de dados local via XanoScript, e precisamos agora criar as APIs REST correspondentes no backend e integrá-las à interface Streamlit.

## Goals / Non-Goals

**Goals:**
- Criar endpoints REST robustos no XanoScript para CRUD completo de tarefas.
- Garantir segurança a nível de registro (Row-Level Security) filtrando sempre as tarefas pelo `user_id` autenticado.
- Substituir a lógica de mock local do Streamlit por chamadas de rede dinâmicas.
- Oferecer opções avançadas de ordenação e agrupamento na interface do usuário (por Disciplina ou por Prazo).
- Implementar sinalização visual clara em vermelho para tarefas expiradas.

**Non-Goals:**
- Envio de e-mails de alerta automáticos ou lembretes por SMS.
- Sincronização automática com calendários externos (como Google Calendar).
- Suporte a subtarefas ou check-lists internos dentro de cada tarefa.

## Decisions

### Estrutura de Endpoints de API

- **POST /academic_task/create**
  - **Função:** Cria uma nova tarefa associada a `subject_id` e ao usuário autenticado (`user_id = $auth.id`).
  - **Status inicial:** Sempre `"pending"`.

- **GET /academic_task/list**
  - **Função:** Retorna todas as tarefas pertencentes ao usuário autenticado.
  - **Filtros opcionais:** `status` (para simplificar a consulta e diminuir o tráfego de dados).

- **PATCH /academic_task/update**
  - **Função:** Atualiza as propriedades editáveis (`title`, `description`, `due_date`, `status`) de uma tarefa após verificar que pertence ao usuário logado.

- **DELETE /academic_task/delete**
  - **Função:** Remove permanentemente a tarefa caso ela pertença ao usuário logado.

### Sinalização Visual de Tarefas Vencidas

- **Decisão:** Realizar o cálculo dinâmico da data atual no frontend Streamlit, comparando a data `due_date` recebida com `datetime.date.today()`.
- **Mitigação visual:** Tarefas cuja data seja anterior a hoje e que tenham status diferente de `"completed"` receberão uma etiqueta estilizada vermelha ("🚨 PRAZO VENCIDO") e borda destacada para atrair a atenção do usuário de imediato.

## Risks / Trade-offs

- **Filtro de Disciplina Geral:** A interface possui tarefas associadas à disciplina "Geral". Como "Geral" é um mock e a tabela no banco exige associação a um `subject_id` válido, no backend as tarefas sem disciplina associada serão vinculadas a um valor nulo/opcional (se permitido) ou o frontend exigirá a seleção de uma disciplina cadastrada para criação física.
- **Formatação de Data:** As datas trafegarão no formato string padrão ISO (`YYYY-MM-DD`). O Streamlit converterá os campos nativos do seletor `st.date_input` sem necessidade de manipulação complexa.
