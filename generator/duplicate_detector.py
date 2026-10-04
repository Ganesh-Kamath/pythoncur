"""
Duplicate Detector for Codolingo Curriculum Generator.
Detects exact duplicates, normalized duplicates, overly similar questions, and repeated patterns.
"""

import re
from typing import Any, Dict, List, Set, Tuple

class DuplicateDetector:
    def __init__(self, similarity_threshold: float = 0.85):
        self.similarity_threshold = similarity_threshold

    @staticmethod
    def normalize(text: str) -> str:
        """Strip formatting, punctuation, and extraneous whitespace for comparison."""
        if not text:
            return ""
        # Lowercase
        text = text.lower()
        # Remove common markdown symbols and non-semantic punctuation, preserving parentheses and math operators
        text = re.sub(r"[`*_#.!?,;\"\'\\]+", " ", text)
        # Collapse whitespace
        text = re.sub(r"\s+", " ", text).strip()
        return text

    @staticmethod
    def get_token_set(text: str) -> Set[str]:
        words = DuplicateDetector.normalize(text).split()
        return {w for w in words if len(w) > 2}

    def compute_jaccard_similarity(self, text1: str, text2: str) -> float:
        """Compute Jaccard similarity between two texts based on word tokens."""
        set1 = self.get_token_set(text1)
        set2 = self.get_token_set(text2)
        if not set1 or not set2:
            return 0.0
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        return intersection / union if union > 0 else 0.0

    def check_lesson_items(self, items: List[Dict[str, Any]]) -> Tuple[List[str], List[str]]:
        """
        Analyze all items in a lesson for duplicate or repetitive content.
        Returns:
            errors: List of severe duplicate violations (e.g. identical prompts)
            warnings: List of potential similarity or repetition warnings
        """
        errors: List[str] = []
        warnings: List[str] = []

        seen_exact_prompts: Dict[str, str] = {}
        seen_normalized_prompts: Dict[str, str] = {}
        seen_solution_codes: Dict[str, str] = {}

        # Track consecutive answer patterns in MCQs
        consecutive_mcq_answers: List[str] = []

        for idx, item in enumerate(items, start=1):
            item_id = item.get("id", f"item_{idx}")
            prompt = item.get("prompt") or item.get("title") or ""
            raw_prompt = prompt.strip()
            norm_prompt = self.normalize(raw_prompt)

            # Check exact duplicates
            if raw_prompt and len(raw_prompt) > 10:
                if raw_prompt in seen_exact_prompts:
                    errors.append(f"{item_id}: Exact duplicate prompt of {seen_exact_prompts[raw_prompt]}")
                else:
                    seen_exact_prompts[raw_prompt] = item_id

            # Check normalized duplicates
            if norm_prompt and len(norm_prompt) > 15:
                if norm_prompt in seen_normalized_prompts:
                    prior_id = seen_normalized_prompts[norm_prompt]
                    if prior_id != seen_exact_prompts.get(raw_prompt):
                        errors.append(f"{item_id}: Normalized duplicate prompt of {prior_id}")
                else:
                    seen_normalized_prompts[norm_prompt] = item_id

            # Check solution_code duplicates
            sol_code = (item.get("solution_code") or "").strip()
            if sol_code and len(sol_code) > 20:
                if sol_code in seen_solution_codes:
                    warnings.append(f"{item_id}: Identical solution code as {seen_solution_codes[sol_code]}")
                else:
                    seen_solution_codes[sol_code] = item_id

            # Track consecutive MCQ answers
            if item.get("type") == "multiple_choice":
                ans = item.get("correct_answer")
                if isinstance(ans, str) and ans in {"A", "B", "C", "D"}:
                    consecutive_mcq_answers.append(ans)
                    if len(consecutive_mcq_answers) >= 6:
                        # If 6 consecutive MCQs have the exact same letter
                        if len(set(consecutive_mcq_answers[-6:])) == 1:
                            warnings.append(f"{item_id}: 6 consecutive multiple choice questions share the same answer ('{ans}')")

        # Fuzzy similarity check across all prompts in the lesson
        items_with_prompts = [
            (it.get("id", f"item_{i}"), (it.get("prompt") or it.get("title") or "").strip())
            for i, it in enumerate(items, start=1)
            if (it.get("prompt") or it.get("title"))
        ]

        for i in range(len(items_with_prompts)):
            id1, p1 = items_with_prompts[i]
            if len(p1) < 25:
                continue
            for j in range(i + 1, len(items_with_prompts)):
                id2, p2 = items_with_prompts[j]
                if len(p2) < 25:
                    continue
                sim = self.compute_jaccard_similarity(p1, p2)
                if sim >= self.similarity_threshold:
                    warnings.append(f"{id2}: Very high similarity ({int(sim * 100)}%) with {id1}")

        return errors, warnings
