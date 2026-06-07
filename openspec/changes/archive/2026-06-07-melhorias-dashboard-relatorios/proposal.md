# melhorias-dashboard-relatorios Specification

## Purpose

Proporcionar ao estudante uma visualização consolidada do seu progresso acadêmico através de um Dashboard de controle, uma tela de Relatórios e análises detalhadas, e a possibilidade de organizar melhor as disciplinas por semestre e as tarefas por prioridade, bem como arquivar disciplinas concluídas e exportar os dados para CSV.

## ADDED Requirements

### Requirement: Academic Dashboard

O sistema SHALL exibir um dashboard para o usuário autenticado contendo métricas e informações consolidadas.

#### Scenario: Usuário com dados visualiza dashboard consolidado
- **WHEN** o usuário autenticado acessa a página inicial (Dashboard) e possui disciplinas cadastradas
- **THEN** o sistema SHALL exibir: o total de disciplinas ativas (status "active"), o total de tarefas pendentes (status "pending" ou "in_progress"), o total de tarefas em atraso (com prazo vencido), o indicador de progresso geral (percentual de tarefas concluídas) e a lista das próximas tarefas com prazo mais próximo ordenadas por data.

#### Scenario: Usuário sem dados visualiza tela de boas-vindas
- **WHEN** o usuário autenticado acessa a página inicial e não possui nenhuma disciplina cadastrada no sistema
- **THEN** o sistema SHALL exibir uma mensagem acolhedora de boas-vindas orientando-o sobre o funcionamento do EduTrack AI e fornecendo um atalho ou instruções para cadastrar sua primeira disciplina.

---

### Requirement: Academic Reports and Data Export

O sistema SHALL disponibilizar uma tela de relatórios com progresso das disciplinas, histórico de tarefas e suporte a exportação de dados em CSV.

#### Scenario: Usuário visualiza progresso e histórico
- **WHEN** o usuário autenticado acessa a tela de Relatórios
- **THEN** o sistema SHALL exibir a taxa de conclusão de tarefas por disciplina (progresso individual) e o histórico de tarefas organizadas por período de tempo.

#### Scenario: Usuário exporta dados acadêmicos para CSV
- **WHEN** o usuário solicita a exportação de seus dados na tela de Relatórios
- **THEN** o sistema SHALL gerar e disponibilizar para download arquivos CSV contendo os dados de suas disciplinas e tarefas acadêmicas.

---

### Requirement: Subject Semester and Archiving

O sistema SHALL permitir associar um semestre ou período letivo às disciplinas e possibilitar o seu arquivamento.

#### Scenario: Usuário associa semestre à disciplina
- **WHEN** o usuário cadastra ou edita uma disciplina informando o semestre/período (ex: "2026.1")
- **THEN** o sistema SHALL salvar a informação do semestre no banco de dados e exibi-la na listagem de disciplinas.

#### Scenario: Usuário arquiva uma disciplina
- **WHEN** o usuário solicita o arquivamento de uma disciplina concluída
- **THEN** o sistema SHALL atualizar o status da disciplina para "archived", ocultando-a da listagem padrão de disciplinas ativas e da contagem de disciplinas no dashboard, mas permitindo sua visualização e restauração em uma área/filtro de arquivados.

---

### Requirement: Task Priority

O sistema SHALL permitir classificar as tarefas acadêmicas por nível de prioridade.

#### Scenario: Usuário define prioridade de tarefa
- **WHEN** o usuário cadastra ou edita uma tarefa selecionando uma prioridade (Baixa, Média, Alta)
- **THEN** o sistema SHALL persistir a prioridade correspondente ("low", "medium", "high") no banco de dados e exibir visualmente a prioridade em destaque no card da tarefa.
