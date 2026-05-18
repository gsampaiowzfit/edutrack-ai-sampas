"""Simple test runner for environments without pytest installed.

This imports the test module and executes functions starting with `test_`.
Exits with code 0 on success, non-zero on failure.
"""
import importlib.util
import inspect
import sys
from pathlib import Path


def run_tests(module_path: str) -> int:
    path = Path(module_path)
    spec = importlib.util.spec_from_file_location(path.stem, path)
    if spec is None or spec.loader is None:
        print(f"Cannot load module from {module_path}")
        return 1
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    funcs = [v for n, v in inspect.getmembers(mod, inspect.isfunction) if n.startswith("test_")]
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
    return failures


if __name__ == "__main__":
    # ensure project root is on sys.path so tests can import top-level modules
    project_root = Path(__file__).resolve().parents[1]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    # module path for the tests
    module_file = project_root / "workflow_tests" / "test_calculate_progress.py"
    failures = run_tests(str(module_file))
    if failures:
        print(f"{failures} test(s) failed")
        sys.exit(1)
    print("All tests passed")
    sys.exit(0)
