"""
Sarvam Reviewer for Codolingo Improvement Engine.
Evaluates proposed curriculum modifications against a rigorous pedagogical quality gate.
"""

import json
import logging
import re
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from curriculum_improver.config import config
from generator.sarvam_client import SarvamClient

logger = logging.getLogger("SarvamReviewer")

@dataclass
class ReviewResult:
    decision: str  # "accept", "revise", "reject"
    conceptual_correctness: int  # 0-100
    pedagogical_quality: int     # 0-100
    difficulty_quality: int      # 0-100
    clarity: int                 # 0-100
    ambiguity: int               # 0-100 (lower is better)
    exercise_alignment: int      # 0-100
    problems: List[str] = field(default_factory=list)
    required_changes: List[str] = field(default_factory=list)
    reasoning_summary: str = ""
    raw_response: Optional[str] = None

    def is_accepted(self, min_overall: int = 75) -> bool:
        """Evaluate if the review strictly meets acceptance criteria."""
        if self.decision.lower() != "accept":
            return False
        if self.conceptual_correctness < 85:
            return False
        if self.ambiguity > 25:
            return False
        avg_score = (self.conceptual_correctness + self.pedagogical_quality + self.clarity + self.exercise_alignment) / 4
        return avg_score >= min_overall

class SarvamReviewer:
    def __init__(self, sarvam_client: Optional[SarvamClient] = None):
        self.client = sarvam_client or SarvamClient()
        self.hourly_call_timestamps: List[float] = []

    def is_online(self) -> bool:
        """Check if Sarvam API key is configured and reachable."""
        return self.client.has_api_key()

    def _check_budget(self) -> bool:
        """Enforce hourly call budget to prevent runaway API spend."""
        now = time.time()
        # Keep calls within last 3600 seconds
        self.hourly_call_timestamps = [t for t in self.hourly_call_timestamps if now - t < 3600]
        if len(self.hourly_call_timestamps) >= config.max_sarvam_calls_per_hour:
            logger.warning(f"Sarvam hourly budget reached ({len(self.hourly_call_timestamps)}/{config.max_sarvam_calls_per_hour}).")
            return False
        return True

    def review_proposed_change(
        self,
        lesson_id: str,
        lesson_title: str,
        concept: str,
        original_item: Optional[Dict[str, Any]],
        proposed_item: Dict[str, Any],
        change_reason: str,
    ) -> ReviewResult:
        """
        Submit a proposed curriculum change to Sarvam for pedagogical quality review.
        """
        if not self._check_budget():
            return ReviewResult(
                decision="reject",
                conceptual_correctness=0,
                pedagogical_quality=0,
                difficulty_quality=0,
                clarity=0,
                ambiguity=100,
                exercise_alignment=0,
                problems=["Hourly Sarvam API budget reached"],
                reasoning_summary="Review delayed due to rate budget control"
            )

        system_prompt = (
            "You are the Chief Curriculum Reviewer for Codolingo. "
            "Critique curriculum items with uncompromising pedagogical and conceptual standards. "
            "Return ONLY valid JSON matching the requested schema."
        )

        orig_str = json.dumps(original_item, indent=2) if original_item else "None (New Exercise Proposal)"
        prop_str = json.dumps(proposed_item, indent=2)

        user_prompt = f"""LESSON: {lesson_id} - {lesson_title}
TARGET CONCEPT: {concept}
REASON FOR IMPROVEMENT: {change_reason}

ORIGINAL ITEM:
{orig_str}

PROPOSED MODIFIED ITEM:
{prop_str}

REVIEW CRITERIA:
1. Conceptual Correctness (0-100): Is the Python explanation and code 100% accurate? Does it avoid misconceptions?
2. Pedagogical Quality (0-100): Does this effectively build understanding and active recall?
3. Difficulty Quality (0-100): Is the labeled difficulty accurate for this stage of learning?
4. Clarity (0-100): Is the prompt concise, direct, and unambiguous?
5. Ambiguity (0-100): Is there any chance a student could reasonably argue another answer? (0 = perfectly unambiguous, 100 = highly ambiguous)
6. Exercise Alignment (0-100): Does it directly test the target concept and skill?

DECISION RULES:
- "accept": Conceptually sound (>=85), unambiguous (<=20), and a clear net improvement over the original item. Minor stylistic differences should be accepted.
- "revise": Substantive factual omission, misleading hint, or awkward phrasing that needs correction before student exposure.
- "reject": Conceptually incorrect, introduces misconceptions, or degrades curriculum quality.

RETURN ONLY THIS JSON SCHEMA:
{{
  "decision": "accept" | "revise" | "reject",
  "conceptual_correctness": 0-100,
  "pedagogical_quality": 0-100,
  "difficulty_quality": 0-100,
  "clarity": 0-100,
  "ambiguity": 0-100,
  "exercise_alignment": 0-100,
  "problems": ["problem 1", ...],
  "required_changes": ["change 1", ...],
  "reasoning_summary": "Concise 1-2 sentence explanation of judgment."
}}"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        try:
            self.hourly_call_timestamps.append(time.time())
            raw = self.client.complete(messages, temperature=0.1, max_tokens=8192)
            parsed = self.client.extract_json(raw)

            return ReviewResult(
                decision=str(parsed.get("decision", "reject")).lower(),
                conceptual_correctness=int(parsed.get("conceptual_correctness", 50)),
                pedagogical_quality=int(parsed.get("pedagogical_quality", 50)),
                difficulty_quality=int(parsed.get("difficulty_quality", 50)),
                clarity=int(parsed.get("clarity", 50)),
                ambiguity=int(parsed.get("ambiguity", 50)),
                exercise_alignment=int(parsed.get("exercise_alignment", 50)),
                problems=list(parsed.get("problems", [])),
                required_changes=list(parsed.get("required_changes", [])),
                reasoning_summary=str(parsed.get("reasoning_summary", "")),
                raw_response=raw,
            )
        except Exception as e:
            logger.warning(f"Sarvam review call failed: {e}")
            return ReviewResult(
                decision="reject",
                conceptual_correctness=0,
                pedagogical_quality=0,
                difficulty_quality=0,
                clarity=0,
                ambiguity=100,
                exercise_alignment=0,
                problems=[f"API Review Exception: {e}"],
                reasoning_summary="API call failure during review",
            )
