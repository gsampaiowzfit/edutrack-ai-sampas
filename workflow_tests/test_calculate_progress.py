import json
import subprocess
import sys

from scripts.calculate_progress import calculate_progress


def test_normal_case():
    res = calculate_progress(3, 5)
    assert res["percentage"] == 60.0
    assert res["completed"] == 3
    assert res["total"] == 5


def test_total_zero():
    res = calculate_progress(1, 0)
    assert res["percentage"] == 0.0
    assert "warning" in res


def test_completed_greater_than_total():
    res = calculate_progress(10, 4)
    assert res["completed"] == 4
    assert res["percentage"] == 100.0


def test_negative_completed():
    res = calculate_progress(-5, 10)
    assert res["completed"] == 0
    assert res["percentage"] == 0.0


def test_cli_output_json():
    # run the CLI and parse JSON output
    proc = subprocess.run([sys.executable, "scripts/calculate_progress.py", "--completed", "3", "--total", "5"], capture_output=True, text=True)
    assert proc.returncode == 0
    obj = json.loads(proc.stdout)
    assert obj["percentage"] == 60.0
