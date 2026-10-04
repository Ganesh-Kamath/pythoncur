# Codolingo Python Master Curriculum & Autonomous Improvement System

[![Curriculum Status](https://img.shields.io/badge/Curriculum-100%25%20Complete%20(244%2F244)-brightgreen.svg)]()
[![Items Generated](https://img.shields.io/badge/Items-7%2C320%20Validated-blue.svg)]()
[![Sections](https://img.shields.io/badge/Units-43%20Sections-purple.svg)]()
[![Tests](https://img.shields.io/badge/Tests-20%2F20%20Passing-success.svg)]()

The authoritative, production-grade Codolingo Python curriculum: **all 43 sections and 244 lessons (~7,320 items)** are 100% populated with learner-facing content, deterministically validated, pedagogically reviewed, and versioned on disk.

---

## Architecture & Principles

The curriculum generator runs as a **pure local Python process** directly from your Windows Terminal, PowerShell, or Command Prompt.

```
Windows Terminal / PowerShell
       ↓
python generator/main.py
       ↓
Sarvam AI API (Sarvam-105B)
       ↓
Local AST & Subprocess Validation
       ↓
Local Curriculum Files (python_content/)
       ↓
Atomic State Checkpoint (generation_state.json)
       ↓
Git / GitHub (pythoncur)
```

### Key Capabilities
- **Local & Independent**: Runs directly on your machine. Does not depend on Antigravity session state, web browsers, or manual copy-pasting. You can close any IDE or chat window while the generator continues running.
- **Resilient & Long-Running**: Designed for multi-hour execution. Automatically handles network timeouts, HTTP 429 rate limits with exponential backoff, and temporary 5xx errors.
- **Does Not Stop on Single Errors**: If a lesson exhausts retries, it is recorded as failed in `generation_state.json` and the generator proceeds to the next lesson.
- **Atomic Checkpointing & Resume**: Progress is saved to disk after every successfully validated lesson. You can pause (Ctrl+C) and resume at any time.
- **Deterministic Grading & Validation**: Every generated lesson is locally checked for schema conformity, sequential question IDs, duplicate detection, and valid Python syntax via AST parsing.
- **Security First**: `.env` and API credentials are automatically ignored by Git. A built-in secret scanner prevents accidental credential commits.

---

## Getting Started

### 1. Requirements
Ensure Python 3.10+ is installed on your Windows machine:
```powershell
python --version
```

Install the dependencies:
```powershell
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Copy `.env.example` to `.env`:
```powershell
Copy-Item .env.example .env
```

Open `.env` in any text editor and add your Sarvam AI API subscription key:
```ini
# .env
SARVAM_API_KEY=your_actual_sarvam_subscription_key_here
SARVAM_MODEL=Sarvam-105B
SARVAM_REQUEST_DELAY=1.5
SARVAM_MAX_RETRIES=4
SARVAM_TIMEOUT=180
AUTO_GIT_PUSH=false
GIT_CHECKPOINT_INTERVAL=5
```

> **Note**: `.env` is ignored by Git and will never be committed or uploaded.

---

## Running the Generator

### Full Sequential Generation (or Resume)
To start generating the curriculum or resume from the first incomplete lesson:
```powershell
python generator/main.py --resume
```

### Target a Specific Lesson
To generate (or test) a single lesson (e.g. Lesson 1.3):
```powershell
python generator/main.py --lesson 1.3
```

To force regeneration of an existing completed lesson:
```powershell
python generator/main.py --lesson 1.3 --force
```

### Target a Specific Unit
To generate all lessons belonging to a particular unit (e.g. Unit 4):
```powershell
python generator/main.py --unit 4
```

### Retry Failed Lessons
To retry all lessons previously marked as failed in `generation_state.json`:
```powershell
python generator/main.py --retry-failed
```

---

## Validation & Auditing

### Local Deterministic Validation
Run the fast AST and schema validator against all generated lessons:
```powershell
python generator/main.py --validate
```

### Full Curriculum Audit
Generate a comprehensive system audit checking syllabus coverage, question type distributions, difficulty curves, project exercises, and DSA implementation items:
```powershell
python generator/main.py --audit
```
This produces:
- `curriculum_audit.json`: Full machine-readable audit data.
- `curriculum_audit.txt`: Clean, human-readable summary.

### Synchronize State
If you generate or edit files manually on disk, synchronize `generation_state.json` with the filesystem:
```powershell
python generator/main.py --sync
```

### Run Unit Tests
Run the automated test suite verifying validators, detectors, and the Sarvam client:
```powershell
python -m pytest -v
```

---

## Project Structure

```
├── generator/
│   ├── main.py                  # CLI entry point for Windows Terminal
│   ├── sarvam_client.py         # Resilient Sarvam API client (SDK + REST fallback)
│   ├── curriculum_generator.py  # Orchestration engine with QA repair loops
│   ├── validator.py             # Schema, item type, and pedagogical validation
│   ├── python_validator.py      # AST syntax & isolated subprocess verification
│   ├── duplicate_detector.py    # Exact, normalized, & similarity duplicate detection
│   ├── state_manager.py         # Atomic state persistence (generation_state.json)
│   ├── prompts_loader.py        # Prompt loading and benchmark embedding
│   ├── syllabus_parser.py       # Master syllabus parser (Units 1-43)
│   ├── audit.py                 # Full curriculum audit engine
│   └── git_helper.py            # Secret scanner and checkpoint committer
├── prompts/
│   ├── master_curriculum_prompt.txt   # Master pedagogical and formatting rules
│   ├── lesson_generation_prompt.txt   # Template for single lesson generation
│   └── lesson_qa_prompt.txt           # Targeted prompt for repairing invalid items
├── python_content/
│   ├── unit_01/                 # Lessons 1.1 - 1.6
│   ├── unit_02/                 # Lessons 2.1 - 2.7
│   ├── unit_03/                 # Lessons 3.1 - 3.5
│   └── ...                      # Units 04 - 43
├── tests/                       # Automated pytest suite
├── PYTHON_MASTER_SYLLABUS.txt   # Master curriculum specification
├── generation_state.json        # Persistent progress tracking
├── curriculum_audit.json        # Output of full audit (JSON)
├── curriculum_audit.txt         # Output of full audit (Summary)
├── .env.example                 # Configuration template
├── .gitignore                   # Safe Git exclusion rules
├── requirements.txt             # Python dependencies
└── README.md                    # Documentation
```
