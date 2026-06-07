# Checklist de Implementação - Melhorias de Dashboard, Relatórios, Disciplinas e Tarefas

## 1. Banco de Dados e APIs (XanoScript)
- [ ] 1.1 Atualizar o esquema da tabela `subject` no arquivo `tables/803444_subject.xs` para incluir o campo opcional `text? semester` e ajustar `status`
- [ ] 1.2 Atualizar o esquema da tabela `academic_tasks` no arquivo `tables/academic_tasks.xs` para incluir o campo opcional `text? priority`
- [ ] 1.3 Atualizar o endpoint de criação de disciplinas em `apis/subjects/3784200_subject_create_POST.xs` para aceitar e persistir o campo `semester`
- [ ] 1.4 Atualizar o endpoint de atualização de disciplinas em `apis/subjects/3784202_subject_update_PATCH.xs` para aceitar e persistir os campos `semester` e `status` (para arquivamento)
- [ ] 1.5 Atualizar o endpoint de criação de tarefas em `apis/academic_tasks/academic_task_create_POST.xs` para aceitar e persistir o campo `priority`
- [ ] 1.6 Atualizar o endpoint de atualização de tarefas em `apis/academic_tasks/academic_task_update_PATCH.xs` para aceitar e persistir o campo `priority`

## 2. Interface e Navegação (Streamlit)
- [ ] 2.1 Criar a página de Relatórios em `pages/Relatorios.py` exibindo histórico de tarefas, progresso por disciplina e botões de exportação para CSV
- [ ] 2.2 Atualizar `app.py` para melhorar o design de login/cadastro, implementar o Dashboard completo (métricas globais, próximas tarefas ordenadas por prazo, tela de boas-vindas se sem disciplinas) e adicionar o link da página de Relatórios ao menu dinâmico
- [ ] 2.3 Atualizar `pages/Disciplinas.py` para aceitar o campo `semester` na criação/edição, exibir o semestre e a barra de progresso individual por disciplina (tarefas concluídas / totais), permitir arquivamento/desarquivamento (status `archived` / `active`) com abas ou filtros separados para arquivados, e garantir a confirmação em modal antes da exclusão
- [ ] 2.4 Atualizar `pages/Tarefas.py` para aceitar o campo `priority` (Baixa, Média, Alta) na criação/edição, renderizar badges/tags coloridas para a prioridade nos cards, e garantir a confirmação de exclusão
