"""
Curriculum Health Tracker for Codolingo Improvement Engine.
Evaluates multi-dimensional pedagogical quality, structural health, and learner metrics.
"""

import math
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from curriculum_improver.laya_analyzer import LayaAnalyzer, LessonLearnerMetrics
from generator.duplicate_detector import DuplicateDetector
from generator.python_validator import PythonValidator

@dataclass
class HealthReport:
    lesson_id: str
    lesson_title: str
    correctness: int
    concept_coverage: int
    difficulty_balance: int
    exercise_diversity: int
    duplicate_score: int
    explanation_quality: int
    prerequisites_quality: int
    learner_success: Optional[int]
    learner_data_status: str  # "measured", "inferred", "unavailable"
    overall_health: int
    findings: List[str] = field(default_factory=list)

    def to_markdown(self) -> str:
        learner_val = f"{self.learner_success}" if self.learner_success is not None else "Unavailable"
        lines = [
            f"## Lesson {self.lesson_id} - {self.lesson_title}",
            "",
            f"{'Correctness':<22} {self.correctness:>3}",
            f"{'Concept coverage':<22} {self.concept_coverage:>3}",
            f"{'Difficulty balance':<22} {self.difficulty_balance:>3}",
            f"{'Exercise diversity':<22} {self.exercise_diversity:>3}",
            f"{'Duplicate score':<22} {self.duplicate_score:>3}",
            f"{'Learner success':<22} {learner_val:>3} ({self.learner_data_status})",
            f"{'Explanation quality':<22} {self.explanation_quality:>3}",
            f"{'Prerequisites':<22} {self.prerequisites_quality:>3}",
            "",
            f"Overall health: {self.overall_health}",
        ]
        if self.findings:
            lines.append("\nKey Findings & Improvement Targets:")
            for f in self.findings:
                lines.append(f"- {f}")
        return "\n".join(lines)

class HealthTracker:
    def __init__(self, laya_analyzer: Optional[LayaAnalyzer] = None):
        self.laya = laya_analyzer or LayaAnalyzer()
        self.py_validator = PythonValidator()
        self.dup_detector = DuplicateDetector()

    def evaluate_lesson(self, lesson_data: Dict[str, Any]) -> HealthReport:
        """Conduct comprehensive multi-dimensional health audit of a lesson."""
        lesson_id = str(lesson_data.get("lesson_id", "unknown"))
        lesson_title = str(lesson_data.get("title", ""))
        items = lesson_data.get("items", [])
        total_items = len(items)

        findings: List[str] = []

        if total_items == 0:
            return HealthReport(
                lesson_id=lesson_id,
                lesson_title=lesson_title,
                correctness=0,
                concept_coverage=0,
                difficulty_balance=0,
                exercise_diversity=0,
                duplicate_score=0,
                explanation_quality=0,
                prerequisites_quality=0,
                learner_success=None,
                learner_data_status="unavailable",
                overall_health=0,
                findings=["Lesson contains 0 items"],
            )

        # 1. Correctness Score (0-100)
        syntax_errors = 0
        structural_errors = 0
        for it in items:
            code_errs, _ = self.py_validator.validate_item_code(it, execute_code=False)
            if code_errs:
                syntax_errors += len(code_errs)
            # Check options vs correct_answer
            itype = it.get("type")
            if itype in {"multiple_choice", "code_prediction", "output_prediction"}:
                opts = it.get("options", [])
                ans = it.get("correct_answer")
                if not ans or not opts:
                    structural_errors += 1

        correctness = max(0, 100 - (syntax_errors * 20 + structural_errors * 10))
        if syntax_errors > 0:
            findings.append(f"{syntax_errors} Python syntax errors detected")

        # 2. Concept Coverage (0-100)
        concepts = {it.get("concept") for it in items if it.get("concept")}
        micro_lessons = [it for it in items if it.get("type") == "micro_lesson"]
        concept_count = len(concepts)
        # Ideal: 3 to 8 distinct sub-concepts per 30 items
        if concept_count < 2:
            concept_coverage = 50
            findings.append("Low concept diversity: only 1 concept identified")
        elif 3 <= concept_count <= 8:
            concept_coverage = min(100, 70 + (len(micro_lessons) * 6))
        else:
            concept_coverage = 85

        # 3. Difficulty Balance (0-100)
        diff_counts = {"easy": 0, "medium": 0, "hard": 0}
        for it in items:
            d = it.get("difficulty", "medium").lower()
            diff_counts[d] = diff_counts.get(d, 0) + 1

        easy_pct = (diff_counts["easy"] / total_items) * 100
        med_pct = (diff_counts["medium"] / total_items) * 100
        hard_pct = (diff_counts["hard"] / total_items) * 100

        # Ideal curve: 30-40% easy, 40-50% medium, 15-25% hard
        diff_penalty = (
            abs(easy_pct - 35) * 0.8 +
            abs(med_pct - 45) * 0.6 +
            abs(hard_pct - 20) * 1.0
        )
        difficulty_balance = max(20, min(100, int(100 - diff_penalty)))
        if hard_pct < 10:
            findings.append("Lack of challenging/hard exercises (<10%)")
        if easy_pct > 60:
            findings.append("Overly easy distribution (>60% easy)")

        # 4. Exercise Diversity (0-100)
        type_counts: Dict[str, int] = {}
        for it in items:
            t = it.get("type", "unknown")
            type_counts[t] = type_counts.get(t, 0) + 1

        distinct_types = len(type_counts)
        # Shannon entropy
        entropy = 0.0
        for count in type_counts.values():
            p = count / total_items
            if p > 0:
                entropy -= p * math.log2(p)

        # Max entropy for 6+ types is ~2.5
        diversity_raw = min(1.0, entropy / 2.3)
        exercise_diversity = max(20, min(100, int(diversity_raw * 100)))
        if distinct_types < 4:
            findings.append(f"Low exercise type variety ({distinct_types} distinct types)")

        # 5. Duplicate Score (0-100)
        dup_errs, dup_warns = self.dup_detector.check_lesson_items(items)
        duplicate_score = max(0, 100 - (len(dup_errs) * 25 + len(dup_warns) * 5))
        if dup_errs:
            findings.append(f"{len(dup_errs)} duplicate prompts detected")

        # 6. Explanation Quality (0-100)
        # Exclude micro_lesson items since they teach via 'content' rather than 'explanation'
        exercise_items = [it for it in items if it.get("type") != "micro_lesson"]
        if exercise_items:
            items_with_explanations = sum(1 for it in exercise_items if it.get("explanation") and len(str(it["explanation"])) > 20)
            expl_pct = (items_with_explanations / len(exercise_items)) * 100
        else:
            expl_pct = 100.0

        explanation_quality = int(expl_pct)
        if expl_pct < 80:
            findings.append(f"Only {int(expl_pct)}% of exercise items have comprehensive explanations")

        # 7. Prerequisites Coherence (0-100)
        seen_ids = set()
        broken_prereqs = 0
        total_prereqs_checked = 0
        for it in items:
            iid = it.get("id")
            for p in it.get("prerequisites", []):
                total_prereqs_checked += 1
                if p not in seen_ids and p != iid:
                    broken_prereqs += 1
            if iid:
                seen_ids.add(iid)

        prerequisites_quality = 100 if total_prereqs_checked == 0 else max(0, 100 - int((broken_prereqs / total_prereqs_checked) * 100))
        if broken_prereqs > 0:
            findings.append(f"{broken_prereqs} forward/broken prerequisite references")

        # 8. Learner Success (measured vs unavailable)
        learner_metrics = self.laya.get_lesson_metrics(lesson_id)
        learner_score: Optional[int] = None
        if learner_metrics.status == "measured":
            learner_score = int(learner_metrics.completion_rate * 100)
            if learner_metrics.high_failure_questions:
                findings.append(f"{len(learner_metrics.high_failure_questions)} questions have >40% learner failure rate")
        else:
            learner_score = None

        # Composite Overall Health Score
        if learner_score is not None:
            overall = int(
                correctness * 0.25 +
                concept_coverage * 0.15 +
                difficulty_balance * 0.10 +
                exercise_diversity * 0.15 +
                duplicate_score * 0.10 +
                explanation_quality * 0.10 +
                prerequisites_quality * 0.05 +
                learner_score * 0.10
            )
        else:
            overall = int(
                correctness * 0.28 +
                concept_coverage * 0.17 +
                difficulty_balance * 0.12 +
                exercise_diversity * 0.17 +
                duplicate_score * 0.11 +
                explanation_quality * 0.10 +
                prerequisites_quality * 0.05
            )

        return HealthReport(
            lesson_id=lesson_id,
            lesson_title=lesson_title,
            correctness=correctness,
            concept_coverage=concept_coverage,
            difficulty_balance=difficulty_balance,
            exercise_diversity=exercise_diversity,
            duplicate_score=duplicate_score,
            explanation_quality=explanation_quality,
            prerequisites_quality=prerequisites_quality,
            learner_success=learner_score,
            learner_data_status=learner_metrics.status,
            overall_health=overall,
            findings=findings,
        )
