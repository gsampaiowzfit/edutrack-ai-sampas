# Checklist de Implementação — Gestão de Tarefas

## 1. Configuração do Backend (XanoScript)
- [ ] 1.1 Criar o arquivo de grupo de APIs `apis/academic_tasks/api_group.xs`
- [ ] 1.2 Criar o endpoint de criação `POST academic_task/create` em `apis/academic_tasks/academic_task_create_POST.xs`
- [ ] 1.3 Criar o endpoint de listagem `GET academic_task/list` em `apis/academic_tasks/academic_task_list_GET.xs`
- [ ] 1.4 Criar o endpoint de atualização `PATCH academic_task/update` em `apis/academic_tasks/academic_task_update_PATCH.xs`
- [ ] 1.5 Criar o endpoint de exclusão `DELETE academic_task/delete` em `apis/academic_tasks/academic_task_delete_DELETE.xs`

## 2. Integração com o Frontend (Streamlit)
- [ ] 2.1 Adicionar a rota do novo grupo de APIs em `utils.py` no dicionário `API_GROUPS`
- [ ] 2.2 Atualizar o fluxo de criação em `pages/Tarefas.py` para fazer a chamada à API `academic_task/create`
- [ ] 2.3 Atualizar o fluxo de listagem em `pages/Tarefas.py` consumindo dados reais da API `academic_task/list`
- [ ] 2.4 Implementar agrupamento dinâmico na interface: agrupar por disciplina ou agrupar por prazo/data
- [ ] 2.5 Atualizar a ação de marcar como concluída/pendente enviando requisição `PATCH` para a API `academic_task/update`
- [ ] 2.6 Implementar a funcionalidade de edição dos dados da tarefa enviando requisição `PATCH` para a API `academic_task/update`
- [ ] 2.7 Atualizar a ação de exclusão enviando requisição `DELETE` para a API `academic_task/delete`
- [ ] 2.8 Implementar o filtro de tarefas por status (Todas, Pendente, Em andamento, Concluída) na barra lateral ou cabeçalho da listagem
- [ ] 2.9 Adicionar checagem local de prazos no frontend e exibir um alerta visual de prazo vencido em vermelho com ícone "🚨" para tarefas expiradas não concluídas

## 3. Testes e Validação
- [ ] 3.1 Criar o arquivo de testes automatizados de workflow em `workflow_tests/test_academic_tasks.py`
- [ ] 3.2 Executar testes locais sem pytest para validar o CRUD e propriedade de dados das tarefas
- [ ] 3.3 Testar manualmente todos os fluxos de interface no Streamlit
