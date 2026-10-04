"""
Python Code Validator for Codolingo Curriculum Generator.
Performs AST syntax validation and isolated subprocess execution with safety controls.
"""

import ast
import os
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

@dataclass
class ExecutionResult:
    success: bool
    stdout: str
    stderr: str
    exit_code: int
    timed_out: bool = False
    error_type: Optional[str] = None

class PythonValidator:
    def __init__(self, timeout_seconds: float = 2.0):
        self.timeout_seconds = timeout_seconds

    def check_syntax(self, code: str, is_placeholder_allowed: bool = False) -> Tuple[bool, Optional[str]]:
        """Validate code syntax using AST parsing."""
        if not code or not code.strip():
            return True, None

        # If placeholders are expected in templates (e.g. fill in the blanks)
        if is_placeholder_allowed:
            if "____" in code or ("<" in code and ">" in code):
                return True, None

        code_to_parse = code.strip()
        # If code is a compound statement header (ends with ':'), add a dummy body
        if code_to_parse.endswith(":") and not code_to_parse.endswith("\\:"):
            code_to_parse += "\n    pass"

        try:
            ast.parse(code_to_parse)
            return True, None
        except SyntaxError as e:
            return False, f"SyntaxError at line {e.lineno}, col {e.offset}: {e.msg}"
        except Exception as e:
            return False, f"ParseError: {str(e)}"

    def get_safe_env(self) -> Dict[str, str]:
        """Create a heavily restricted environment dictionary without access to secrets or .env."""
        safe_env = {}
        # Keep minimal OS required variables on Windows
        for key in ["SYSTEMROOT", "WINDIR", "PATH", "COMSPEC", "TEMP", "TMP"]:
            if key in os.environ:
                safe_env[key] = os.environ[key]

        # Explicitly ensure sensitive tokens are NOT passed
        for forbidden in ["SARVAM_API_KEY", "OPENAI_API_KEY", "ANTHROPIC_API_KEY"]:
            safe_env.pop(forbidden, None)

        safe_env["PYTHONSAFEPATH"] = "1"
        safe_env["PYTHONDONTWRITEBYTECODE"] = "1"
        return safe_env

    def run_code_isolated(self, code: str) -> ExecutionResult:
        """Execute Python code in an isolated subprocess with timeout and safety constraints."""
        safe_env = self.get_safe_env()

        # Run within an isolated temporary directory so local workspace files (.env, etc.) cannot be accessed
        with tempfile.TemporaryDirectory() as sandbox_dir:
            temp_script = Path(sandbox_dir) / "snippet.py"
            temp_script.write_text(code, encoding="utf-8")

            cmd = [
                sys.executable,
                "-I",  # Isolated mode: no user site directory, ignore environment variables
                str(temp_script)
            ]

            try:
                proc = subprocess.run(
                    cmd,
                    cwd=sandbox_dir,
                    env=safe_env,
                    capture_output=True,
                    text=True,
                    timeout=self.timeout_seconds,
                    shell=False
                )
                
                # Check for Python exceptions in stderr
                error_type = None
                if proc.returncode != 0 and proc.stderr:
                    for line in proc.stderr.splitlines():
                        if "Error:" in line or "Exception:" in line:
                            error_type = line.split(":")[0].strip()

                return ExecutionResult(
                    success=(proc.returncode == 0),
                    stdout=proc.stdout,
                    stderr=proc.stderr,
                    exit_code=proc.returncode,
                    timed_out=False,
                    error_type=error_type,
                )
            except subprocess.TimeoutExpired:
                return ExecutionResult(
                    success=False,
                    stdout="",
                    stderr=f"Execution timed out after {self.timeout_seconds} seconds",
                    exit_code=-1,
                    timed_out=True,
                    error_type="TimeoutExpired",
                )
            except Exception as e:
                return ExecutionResult(
                    success=False,
                    stdout="",
                    stderr=str(e),
                    exit_code=-1,
                    error_type=type(e).__name__,
                )

    def validate_item_code(self, item: Dict[str, Any], execute_code: bool = False) -> Tuple[List[str], List[str]]:
        """Validate code fields inside a curriculum item."""
        errors: List[str] = []
        warnings: List[str] = []
        item_id = item.get("id", "unknown_item")
        itype = item.get("type", "")

        # 1. Validate solution_code syntax and execution
        solution_code = item.get("solution_code")
        if solution_code:
            valid_syntax, err = self.check_syntax(solution_code, is_placeholder_allowed=False)
            if not valid_syntax:
                errors.append(f"{item_id}: solution_code syntax error: {err}")
            elif execute_code:
                # If code is small and self-contained (does not ask for interactive input), test run it
                if "input(" not in solution_code and "while True" not in solution_code and "sleep(" not in solution_code:
                    res = self.run_code_isolated(solution_code)
                    if not res.success and not res.timed_out:
                        warnings.append(f"{item_id}: solution_code execution warning: {res.stderr.strip()[:100]}")

        # 2. Validate starter_code
        starter_code = item.get("starter_code")
        if starter_code:
            is_intentional_bug = itype in {"fix_the_code", "error_diagnosis"}
            is_template = "____" in starter_code or ("<" in starter_code and ">" in starter_code)
            
            valid_syntax, err = self.check_syntax(starter_code, is_placeholder_allowed=is_template or is_intentional_bug)
            if not valid_syntax and not is_intentional_bug and not is_template:
                warnings.append(f"{item_id}: starter_code syntax error: {err}")

        # 3. Validate standalone code snippet
        code_snippet = item.get("code")
        if code_snippet:
            is_template = "____" in code_snippet or ("<" in code_snippet and ">" in code_snippet)
            is_bug_demo = itype in {"error_diagnosis", "fix_the_code"}
            valid_syntax, err = self.check_syntax(code_snippet, is_placeholder_allowed=is_template or is_bug_demo)
            if not valid_syntax and not is_template and not is_bug_demo:
                warnings.append(f"{item_id}: code snippet syntax error: {err}")

        return errors, warnings
