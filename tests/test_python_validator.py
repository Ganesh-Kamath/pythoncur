"""
Unit tests for PythonValidator.
"""

from generator.python_validator import PythonValidator

def test_valid_syntax():
    pv = PythonValidator()
    valid, err = pv.check_syntax("x = 10\nprint(x * 2)")
    assert valid is True
    assert err is None

def test_invalid_syntax():
    pv = PythonValidator()
    valid, err = pv.check_syntax("if True\n    x = 1")
    assert valid is False
    assert "SyntaxError" in err

def test_isolated_execution_success():
    pv = PythonValidator()
    res = pv.run_code_isolated("print('ANTIGRAVITY_TEST_SUCCESS')")
    assert res.success is True
    assert "ANTIGRAVITY_TEST_SUCCESS" in res.stdout
    assert res.exit_code == 0

def test_isolated_execution_timeout():
    pv = PythonValidator(timeout_seconds=0.5)
    res = pv.run_code_isolated("import time\ntime.sleep(2)")
    assert res.success is False
    assert res.timed_out is True
