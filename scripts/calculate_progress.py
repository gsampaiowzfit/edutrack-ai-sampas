"""Calculate progress percentage and provide a CLI.

Public API:
  - calculate_progress(completed: int, total: int) -> dict

CLI usage:
  python scripts/calculate_progress.py --completed 3 --total 5

Outputs JSON to stdout.
"""
from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Dict


def _to_int(value: Any) -> int:
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        if value.is_integer():
            return int(value)
        raise ValueError("value must be an integer")
    if isinstance(value, str):
        if value.strip() == "":
            raise ValueError("empty string")
        try:
            return int(value)
        except ValueError:
            try:
                f = float(value)
            except ValueError:
                raise ValueError(f"cannot convert {value!r} to int")
            if f.is_integer():
                return int(f)
            raise ValueError("value must be an integer")
    raise ValueError("unsupported type for integer conversion")


def calculate_progress(completed: Any, total: Any) -> Dict[str, Any]:
    """Calculate progress percentage.

    completed and total are converted to integers when possible. For invalid
    conversions a ValueError is raised.

    Returns a dict suitable for JSON serialization.
    """
    c = _to_int(completed)
    t = _to_int(total)

    if t <= 0:
        return {
            "completed": max(0, c),
            "total": t,
            "percentage": 0.0,
            "unit": "%",
            "warning": "total must be > 0",
        }

    # clamp completed
    if c < 0:
        c = 0
    if c > t:
        c = t

    percentage = round((c / t) * 100.0, 2)
    return {"completed": c, "total": t, "percentage": percentage, "unit": "%"}


def _cli_main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Calculate progress percentage and output JSON")
    parser.add_argument("--completed", required=True, help="Completed count")
    parser.add_argument("--total", required=True, help="Total count")
    args = parser.parse_args(argv)

    try:
        result = calculate_progress(args.completed, args.total)
    except Exception as exc:
        err = {"error": str(exc)}
        print(json.dumps(err))
        return 2

    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(_cli_main())
