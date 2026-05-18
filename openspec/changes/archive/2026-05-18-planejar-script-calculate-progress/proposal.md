# planejar-script-calculate-progress Proposal

## Purpose

Planejar a implementação de um script Python em `scripts/calculate_progress.py` que calcule a porcentagem de progresso (concluídas / total) e retorne um JSON.

## What (O que será feito)

- Implementar a função `calculate_progress(completed: int, total: int) -> dict` que retorna um objeto JSON com a porcentagem (0-100) arredondada e metadados.
- Fornecer interface de linha de comando e importável como módulo (ex.: `python scripts/calculate_progress.py --completed 3 --total 5` ou `from scripts.calculate_progress import calculate_progress`).
- Tratar casos de borda (total = 0, valores negativos, tipos inválidos) de forma defensiva.

## Why (Por que)

Um utilitário simples para calcular progresso é útil para várias partes do sistema (páginas, APIs e tarefas) que exibem progresso de atividades, tarefas ou avaliações. Centralizar a lógica evita inconsistências no cálculo e no tratamento de casos extremos.

## Scope (Escopo)

Inclui somente a criação do script e testes unitários básicos. Não inclui integração com APIs, deploy, ou alterações em outros módulos.

## Impact

- Arquivo criado: `scripts/calculate_progress.py`
- Testes criados: `workflow_tests/test_calculate_progress.py` (opcional, recomendado)
