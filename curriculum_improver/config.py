"""
Configuration for Codolingo Continuous Curriculum Improvement Engine.
Loads environment variables safely and defines system constraints.
"""

import os
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv

# Ensure .env is loaded
load_dotenv(override=True)

@dataclass
class ImproverConfig:
    # Sarvam Reviewer
    sarvam_api_key: str = os.getenv("SARVAM_API_KEY", "").strip()
    sarvam_model: str = os.getenv("SARVAM_MODEL", "sarvam-105b").strip().lower()
    sarvam_timeout: float = float(os.getenv("SARVAM_TIMEOUT", "180"))
    max_sarvam_calls_per_cycle: int = int(os.getenv("MAX_SARVAM_CALLS_PER_CYCLE", "2"))
    max_sarvam_calls_per_hour: int = int(os.getenv("MAX_SARVAM_CALLS_PER_HOUR", "30"))

    # Local Ollama / Qwen3
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434").strip()
    ollama_model: str = os.getenv("OLLAMA_MODEL", "qwen3:8b").strip()
    ollama_timeout: float = float(os.getenv("OLLAMA_TIMEOUT", "15"))
    max_generations_per_cycle: int = int(os.getenv("MAX_GENERATIONS_PER_CYCLE", "3"))

    # Engine Tuning
    sleep_between_cycles: float = float(os.getenv("SLEEP_BETWEEN_CYCLES", "3.0"))
    laya_data_dir: Path = Path(os.getenv("LAYA_DATA_DIR", "data/learner"))

    # Storage Paths
    content_dir: Path = Path("python_content")
    data_dir: Path = Path("data/curriculum")
    versions_dir: Path = Path("data/curriculum/versions")
    logs_dir: Path = Path("data/curriculum/improvement_logs")
    rejected_dir: Path = Path("data/curriculum/rejected_changes")
    reports_dir: Path = Path("data/curriculum/reports")
    db_path: Path = Path("data/curriculum_lab.db")

    def ensure_directories(self) -> None:
        """Create all required data and logging directories."""
        for path in [
            self.content_dir,
            self.data_dir,
            self.versions_dir,
            self.logs_dir,
            self.rejected_dir,
            self.reports_dir,
            self.laya_data_dir,
            self.db_path.parent,
        ]:
            path.mkdir(parents=True, exist_ok=True)

# Global default configuration instance
config = ImproverConfig()
