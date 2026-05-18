# Design: scripts/calculate_progress.py

## Overview

Implementar um módulo Python leve com:

- Função pública `calculate_progress(completed: int, total: int) -> dict`.
- Entrada aceita: inteiros não-negativos; aceitará conversão de strings numéricas quando invocado via CLI.
- Saída: dicionário pronto para serializar em JSON com chaves: `completed`, `total`, `percentage`, `unit`.

## Function contract

- Signature: `def calculate_progress(completed: int, total: int) -> dict`
- Behavior:
  - If `total <= 0`: return `percentage` = 0.0 and include `warning` message.
  - Clamp `completed` between 0 and `total`.
  - Compute percentage as `(completed / total) * 100` (when total > 0) and round to 2 decimal places.

## Output example

```
{
  "completed": 3,
  "total": 5,
  "percentage": 60.0,
  "unit": "%"
}
```

## CLI

- Provide a simple CLI with argparse accepting `--completed`, `--total` or JSON via stdin.
- Output JSON to stdout.

## Error handling

- Type errors: return non-zero exit code and print JSON with `error` key when run as CLI.
- For library usage, raise `ValueError` on invalid non-convertible inputs.

## Tests

- Unit tests to cover: normal case, `total=0`, `completed > total`, negative inputs, non-integer numeric strings.

## Files

- `scripts/calculate_progress.py` — implementation and CLI
- `workflow_tests/test_calculate_progress.py` — unit tests (pytest)
