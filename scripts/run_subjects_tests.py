import importlib.util
from pathlib import Path
p = Path('workflow_tests/test_subjects_ownership.py')
if not p.exists():
    print('test file not found')
    raise SystemExit(2)
spec = importlib.util.spec_from_file_location(p.stem, str(p))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
funcs = [v for n, v in mod.__dict__.items() if callable(v) and n.startswith('test_')]
failures = 0
for func in funcs:
    try:
        func()
        print(f"✓ {func.__name__}")
    except AssertionError as e:
        failures += 1
        print(f"✗ {func.__name__}: AssertionError: {e}")
    except Exception as e:
        failures += 1
        print(f"✗ {func.__name__}: Exception: {e}")
if failures:
    print(f"{failures} test(s) failed")
    raise SystemExit(1)
print('All tests passed')
