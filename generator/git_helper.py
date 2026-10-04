"""
Git Helper & Secret Scanner for Codolingo Curriculum Generator.
Provides safe checkpointing and secret scanning to prevent accidental credential leakage.
"""

import os
import re
import subprocess
from pathlib import Path
from typing import List, Optional, Tuple

FORBIDDEN_PATTERNS = [
    re.compile(r"SARVAM_API_KEY\s*=\s*['\"][a-zA-Z0-9_\-]{8,}['\"]", re.IGNORECASE),
    re.compile(r"api[_-]?key\s*[:=]\s*['\"][a-zA-Z0-9_\-]{16,}['\"]", re.IGNORECASE),
    re.compile(r"sk-[a-zA-Z0-9]{20,}", re.IGNORECASE),
    re.compile(r"-----BEGIN (?:RSA )?PRIVATE KEY-----"),
    re.compile(r"ghp_[a-zA-Z0-9]{20,}"),
]

class GitHelper:
    def __init__(self, repo_dir: Optional[Path] = None):
        self.repo_dir = Path(repo_dir or ".").resolve()
        self.auto_push = os.getenv("AUTO_GIT_PUSH", "false").lower() in {"1", "true", "yes"}

    def run_git(self, args: List[str]) -> Tuple[int, str, str]:
        """Execute a git command within the repository."""
        proc = subprocess.run(
            ["git"] + args,
            cwd=str(self.repo_dir),
            capture_output=True,
            text=True,
            shell=False
        )
        return proc.returncode, proc.stdout.strip(), proc.stderr.strip()

    def scan_for_secrets(self, staged_only: bool = True) -> Tuple[bool, List[str]]:
        """
        Scan git diff for exposed API keys or credentials.
        Returns:
            (is_safe, list_of_violations)
        """
        violations: List[str] = []
        diff_args = ["diff", "--cached"] if staged_only else ["diff"]
        code, stdout, stderr = self.run_git(diff_args)

        if code != 0:
            return False, [f"Failed to run git diff: {stderr}"]

        for line_num, line in enumerate(stdout.splitlines(), start=1):
            if line.startswith("+") and not line.startswith("+++"):
                for pattern in FORBIDDEN_PATTERNS:
                    if pattern.search(line):
                        # Mask matched portion for safe logging
                        violations.append(f"Potential secret detected on diff line {line_num}")

        return (len(violations) == 0), violations

    def checkpoint(self, commit_message: str, force_push: bool = False) -> bool:
        """Stage curriculum changes, run secret scan, commit, and optionally push."""
        # 1. Add curriculum and state files
        self.run_git(["add", "python_content", "generation_state.json", "manifest.json"])

        # 2. Secret scan on staged diff
        is_safe, violations = self.scan_for_secrets(staged_only=True)
        if not is_safe:
            print(f"[Git Security ALERT] Aborting commit! Secret scan failed:")
            for v in violations:
                print(f"  - {v}")
            return False

        # 3. Check if there are staged changes
        code, status, _ = self.run_git(["status", "--porcelain"])
        if not status:
            return True  # Nothing to commit

        # 4. Commit
        code, out, err = self.run_git(["commit", "-m", commit_message])
        if code != 0:
            print(f"[Git Checkpoint] Commit failed: {err}")
            return False

        print(f"[Git Checkpoint] Committed: {commit_message}")

        # 5. Push if enabled
        if self.auto_push or force_push:
            print("[Git Checkpoint] Pushing to remote origin...")
            code, out, err = self.run_git(["push", "origin", "main"])
            if code != 0:
                # Try default branch
                code, out, err = self.run_git(["push", "origin", "HEAD"])
            if code == 0:
                print("[Git Checkpoint] Push successful.")
                return True
            else:
                print(f"[Git Checkpoint] Push warning: {err}")
                return False

        return True
