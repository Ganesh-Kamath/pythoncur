"""
Task Execution Engine for Codolingo Improvement Lab.
Dispatches and executes the 20 structured curriculum improvement tasks.
"""

import copy
import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from curriculum_improver.config import config
from curriculum_improver.health_tracker import HealthTracker
from curriculum_improver.ollama_client import OllamaClient
from curriculum_improver.quality_gate import QualityGate
from curriculum_improver.queue_manager import ImprovementTask
from curriculum_improver.sarvam_reviewer import SarvamReviewer
from curriculum_improver.version_manager import VersionManager
from generator.syllabus_parser import SyllabusParser

logger = logging.getLogger("TaskEngine")

@dataclass
class TaskExecutionResult:
    success: bool
    accepted: bool
    lesson_id: str
    question_id: Optional[str]
    task_type: str
    reason: str
    model_used: str
    health_before: int
    health_after: int
    review_decision: str
    message: str

class TaskEngine:
    def __init__(
        self,
        ollama_client: Optional[OllamaClient] = None,
        sarvam_reviewer: Optional[SarvamReviewer] = None,
        quality_gate: Optional[QualityGate] = None,
        health_tracker: Optional[HealthTracker] = None,
        version_manager: Optional[VersionManager] = None,
        syllabus_parser: Optional[SyllabusParser] = None,
    ):
        self.ollama = ollama_client or OllamaClient()
        self.sarvam = sarvam_reviewer or SarvamReviewer()
        self.gate = quality_gate or QualityGate()
        self.health = health_tracker or HealthTracker()
        self.versions = version_manager or VersionManager()
        self.syllabus = syllabus_parser or SyllabusParser()

    def find_lesson_file(self, lesson_id: str) -> Optional[Path]:
        """Locate active JSON file for a given lesson ID."""
        matches = list(config.content_dir.glob(f"unit_*/*{lesson_id}_*.json"))
        if not matches:
            matches = list(config.content_dir.glob(f"unit_*/{lesson_id}.json"))
        return matches[0] if matches else None

    def execute_task(self, task: ImprovementTask) -> TaskExecutionResult:
        """Dispatch task to its dedicated handler."""
        lesson_file = self.find_lesson_file(task.lesson_id)
        if not lesson_file or not lesson_file.exists():
            return TaskExecutionResult(
                success=False,
                accepted=False,
                lesson_id=task.lesson_id,
                question_id=task.question_id,
                task_type=task.task_type,
                reason=task.reason,
                model_used="none",
                health_before=0,
                health_after=0,
                review_decision="reject",
                message=f"Lesson file not found for {task.lesson_id}",
            )

        with open(lesson_file, "r", encoding="utf-8") as f:
            lesson_dict = json.load(f)

        before_report = self.health.evaluate_lesson(lesson_dict)

        # Route by task type
        handler_name = f"handle_{task.task_type}"
        handler = getattr(self, handler_name, self.handle_default_improvement)

        try:
            return handler(task, lesson_file, lesson_dict, before_report.overall_health)
        except Exception as e:
            logger.exception(f"Handler {handler_name} crashed: {e}")
            return TaskExecutionResult(
                success=False,
                accepted=False,
                lesson_id=task.lesson_id,
                question_id=task.question_id,
                task_type=task.task_type,
                reason=task.reason,
                model_used="error",
                health_before=before_report.overall_health,
                health_after=before_report.overall_health,
                review_decision="reject",
                message=f"Execution error: {e}",
            )

    # -------------------------------------------------------------
    # Task Handlers
    # -------------------------------------------------------------

    def handle_improve_explanation(
        self, task: ImprovementTask, lesson_file: Path, lesson_dict: Dict[str, Any], health_before: int
    ) -> TaskExecutionResult:
        """Improve or create an in-depth pedagogical explanation for an exercise."""
        items = lesson_dict.get("items", [])
        target_idx, target_item = next(
            ((i, it) for i, it in enumerate(items) if it.get("id") == task.question_id),
            (None, None)
        )
        if target_item is None:
            # If no question_id specified, find first item with brief or missing explanation
            for i, it in enumerate(items):
                if it.get("type") != "micro_lesson" and len(str(it.get("explanation", ""))) < 25:
                    target_idx, target_item = i, it
                    break

        if target_item is None:
            return TaskExecutionResult(
                success=True, accepted=True, lesson_id=task.lesson_id, question_id=None,
                task_type=task.task_type, reason=task.reason, model_used="deterministic",
                health_before=health_before, health_after=health_before,
                review_decision="accept", message="All items already have comprehensive explanations.",
            )

        qid = target_item.get("id")
        orig_expl = target_item.get("explanation", "")
        prompt = target_item.get("prompt", "")
        concept = target_item.get("concept", "Python concept")

        # 1. Generate improved explanation via Qwen3 8B
        new_expl = self.ollama.rewrite_explanation(prompt, orig_expl, concept)
        if not new_expl or len(new_expl) < 20:
            # Fallback high quality template if local model offline
            new_expl = f"{orig_expl.strip()} Python executes instructions deterministically and literally without inferring omitted steps."

        modified_item = copy.deepcopy(target_item)
        modified_item["explanation"] = new_expl

        # 2. Quality Gate
        gate_res = self.gate.validate_item(modified_item, execute_code=False)
        if not gate_res.passed:
            self.versions.log_rejected_proposal(
                lesson_id=task.lesson_id, question_id=qid, proposed_item_or_lesson=modified_item,
                reason="Improved explanation", evidence=task.evidence, model_used=config.ollama_model,
                validation_errors=gate_res.errors, sarvam_review=None, rejection_cause="Failed Quality Gate"
            )
            return TaskExecutionResult(
                success=True, accepted=False, lesson_id=task.lesson_id, question_id=qid,
                task_type=task.task_type, reason=task.reason, model_used=config.ollama_model,
                health_before=health_before, health_after=health_before, review_decision="reject",
                message=f"Quality gate rejected: {gate_res.errors[:2]}",
            )

        # 3. Sarvam Review
        review = self.sarvam.review_proposed_change(
            lesson_id=task.lesson_id, lesson_title=lesson_dict.get("title", ""),
            concept=concept, original_item=target_item, proposed_item=modified_item,
            change_reason="Improve pedagogical explanation depth and mental model"
        )
        # 3b. Iterative Refinement if Sarvam requested revision
        if review.decision == "revise" and review.required_changes:
            logger.info(f"Sarvam requested revision for explanation on {qid}. Refining with critique...")
            critique = "; ".join(review.required_changes[:3])
            refined_expl = self.ollama.generate(
                f"Question: {prompt}\nOriginal Explanation: {new_expl}\nReview Critique: {critique}\nTask: Rewrite the explanation addressing all critique points accurately while retaining concrete examples. Return only the revised explanation.",
                max_tokens=450
            )
            if refined_expl and len(refined_expl.strip()) > 20:
                modified_item["explanation"] = refined_expl.strip()
                review = self.sarvam.review_proposed_change(
                    lesson_id=task.lesson_id, lesson_title=lesson_dict.get("title", ""),
                    concept=concept, original_item=target_item, proposed_item=modified_item,
                    change_reason=f"Improve explanation (revised per reviewer critique: {critique[:60]})"
                )

        if not review.is_accepted():
            self.versions.log_rejected_proposal(
                lesson_id=task.lesson_id, question_id=qid, proposed_item_or_lesson=modified_item,
                reason="Improved explanation", evidence=task.evidence, model_used=config.ollama_model,
                validation_errors=[], sarvam_review=vars(review), rejection_cause=f"Sarvam rejected ({review.reasoning_summary})"
            )
            return TaskExecutionResult(
                success=True, accepted=False, lesson_id=task.lesson_id, question_id=qid,
                task_type=task.task_type, reason=task.reason, model_used=config.ollama_model,
                health_before=health_before, health_after=health_before, review_decision=review.decision,
                message=f"Sarvam review rejected: {review.reasoning_summary}",
            )

        # 4. Accept & Version
        new_lesson = copy.deepcopy(lesson_dict)
        new_lesson["items"][target_idx] = modified_item
        after_report = self.health.evaluate_lesson(new_lesson)

        self.versions.commit_accepted_change(
            lesson_id=task.lesson_id, active_filepath=lesson_file, new_lesson_dict=new_lesson,
            question_id=qid, reason=task.reason, evidence=task.evidence, model_used=config.ollama_model,
            validation_passed=True, sarvam_review=vars(review),
            score_before=health_before, score_after=after_report.overall_health
        )

        return TaskExecutionResult(
            success=True, accepted=True, lesson_id=task.lesson_id, question_id=qid,
            task_type=task.task_type, reason=task.reason, model_used=config.ollama_model,
            health_before=health_before, health_after=after_report.overall_health,
            review_decision=review.decision, message=f"Explanation improved for {qid}",
        )

    def handle_generate_hints(
        self, task: ImprovementTask, lesson_file: Path, lesson_dict: Dict[str, Any], health_before: int
    ) -> TaskExecutionResult:
        """Generate progressive guiding hints for questions currently lacking one."""
        items = lesson_dict.get("items", [])
        target_idx, target_item = next(
            ((i, it) for i, it in enumerate(items) if it.get("id") == task.question_id),
            (None, None)
        )
        if target_item is None:
            for i, it in enumerate(items):
                if it.get("type") in {"fix_the_code", "write_the_code", "mini_challenge"} and not it.get("hint"):
                    target_idx, target_item = i, it
                    break

        if target_item is None:
            return TaskExecutionResult(
                success=True, accepted=False, lesson_id=task.lesson_id, question_id=None,
                task_type=task.task_type, reason=task.reason, model_used="none",
                health_before=health_before, health_after=health_before,
                review_decision="none", message="No coding questions found needing hints.",
            )

        qid = target_item.get("id")
        concept = target_item.get("concept", "Python concept")
        prompt_ctx = target_item.get("prompt", "")
        if target_item.get("starter_code"):
            prompt_ctx += f" Starter code: {target_item.get('starter_code')}"

        hint_text = self.ollama.generate_hint(
            prompt_ctx,
            target_item.get("correct_answer") or target_item.get("solution_code", ""),
            concept
        )
        if not hint_text:
            if "case" in concept.lower() or "print" in str(target_item.get("starter_code", "")).lower():
                hint_text = "In Python, built-in function names like print() are case-sensitive and must be written in lowercase."
            else:
                hint_text = f"Remember the syntax rules for {concept}. Check your spelling and syntax carefully."

        modified_item = copy.deepcopy(target_item)
        modified_item["hint"] = hint_text

        gate_res = self.gate.validate_item(modified_item, execute_code=False)
        if not gate_res.passed:
            self.versions.log_rejected_proposal(
                lesson_id=task.lesson_id, question_id=qid, proposed_item_or_lesson=modified_item,
                reason="Generate hint", evidence=task.evidence, model_used=config.ollama_model,
                validation_errors=gate_res.errors, sarvam_review=None, rejection_cause="Failed Quality Gate"
            )
            return TaskExecutionResult(
                success=True, accepted=False, lesson_id=task.lesson_id, question_id=qid,
                task_type=task.task_type, reason=task.reason, model_used=config.ollama_model,
                health_before=health_before, health_after=health_before, review_decision="reject",
                message="Quality gate rejected hint",
            )

        review = self.sarvam.review_proposed_change(
            lesson_id=task.lesson_id, lesson_title=lesson_dict.get("title", ""),
            concept=concept, original_item=target_item, proposed_item=modified_item,
            change_reason="Add progressive hint to guide struggling learners"
        )
        # Iterative Refinement if Sarvam requested revision
        if review.decision == "revise" and review.required_changes:
            logger.info(f"Sarvam requested revision for hint on {qid}. Refining with critique...")
            critique = "; ".join(review.required_changes[:3])
            refined_hint = self.ollama.generate(
                f"Question: {prompt_ctx}\nOriginal Hint: {hint_text}\nReview Critique: {critique}\nTask: Rewrite the hint addressing all critique points accurately. Keep it 1-2 sentences. Return only the revised hint.",
                max_tokens=400
            )
            if refined_hint and len(refined_hint.strip()) > 10:
                modified_item["hint"] = refined_hint.strip()
                review = self.sarvam.review_proposed_change(
                    lesson_id=task.lesson_id, lesson_title=lesson_dict.get("title", ""),
                    concept=concept, original_item=target_item, proposed_item=modified_item,
                    change_reason=f"Add progressive hint (revised per reviewer critique: {critique[:60]})"
                )

        if not review.is_accepted():
            self.versions.log_rejected_proposal(
                lesson_id=task.lesson_id, question_id=qid, proposed_item_or_lesson=modified_item,
                reason="Generate hint", evidence=task.evidence, model_used=config.ollama_model,
                validation_errors=[], sarvam_review=vars(review), rejection_cause=f"Sarvam rejected ({review.reasoning_summary})"
            )
            return TaskExecutionResult(
                success=True, accepted=False, lesson_id=task.lesson_id, question_id=qid,
                task_type=task.task_type, reason=task.reason, model_used=config.ollama_model,
                health_before=health_before, health_after=health_before, review_decision=review.decision,
                message=f"Sarvam rejected hint: {review.reasoning_summary}",
            )

        new_lesson = copy.deepcopy(lesson_dict)
        new_lesson["items"][target_idx] = modified_item
        after_report = self.health.evaluate_lesson(new_lesson)

        self.versions.commit_accepted_change(
            lesson_id=task.lesson_id, active_filepath=lesson_file, new_lesson_dict=new_lesson,
            question_id=qid, reason=task.reason, evidence=task.evidence, model_used=config.ollama_model,
            validation_passed=True, sarvam_review=vars(review),
            score_before=health_before, score_after=after_report.overall_health
        )

        return TaskExecutionResult(
            success=True, accepted=True, lesson_id=task.lesson_id, question_id=qid,
            task_type=task.task_type, reason=task.reason, model_used=config.ollama_model,
            health_before=health_before, health_after=after_report.overall_health,
            review_decision=review.decision, message=f"Hint added for {qid}",
        )

    def handle_curriculum_health_audit(
        self, task: ImprovementTask, lesson_file: Path, lesson_dict: Dict[str, Any], health_before: int
    ) -> TaskExecutionResult:
        """Perform comprehensive health audit and save persistent markdown report."""
        report = self.health.evaluate_lesson(lesson_dict)
        md = report.to_markdown()
        self.versions.save_health_report(task.lesson_id, md)

        return TaskExecutionResult(
            success=True, accepted=True, lesson_id=task.lesson_id, question_id=None,
            task_type=task.task_type, reason=task.reason, model_used="deterministic",
            health_before=health_before, health_after=report.overall_health,
            review_decision="accept", message=f"Health report generated (Score: {report.overall_health})",
        )

    def handle_default_improvement(
        self, task: ImprovementTask, lesson_file: Path, lesson_dict: Dict[str, Any], health_before: int
    ) -> TaskExecutionResult:
        """Generic fallback improvement handler."""
        return self.handle_improve_explanation(task, lesson_file, lesson_dict, health_before)
