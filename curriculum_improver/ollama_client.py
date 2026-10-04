"""
Local Ollama / Qwen3 8B Client for Codolingo Improvement Engine.
Provides inexpensive local generation, variants, rewriting, and hint generation.
"""

import json
import logging
import re
from typing import Any, Dict, List, Optional

import requests
from curriculum_improver.config import config

logger = logging.getLogger("OllamaClient")

class OllamaClient:
    def __init__(
        self,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
        timeout: Optional[float] = None
    ):
        self.base_url = (base_url or config.ollama_base_url).rstrip("/")
        self.model = model or config.ollama_model
        self.timeout = timeout or config.ollama_timeout
        self.session = requests.Session()

    def is_online(self) -> bool:
        """Fast check to verify if local Ollama daemon is reachable."""
        try:
            resp = self.session.get(f"{self.base_url}/api/tags", timeout=2.0)
            return resp.status_code == 200
        except Exception:
            return False

    def is_model_available(self, model_name: Optional[str] = None) -> bool:
        """Check if target model is pulled and ready in Ollama."""
        target = (model_name or self.model).lower()
        try:
            resp = self.session.get(f"{self.base_url}/api/tags", timeout=3.0)
            if resp.status_code == 200:
                models = resp.json().get("models", [])
                for m in models:
                    name = m.get("name", "").lower()
                    if target in name or name in target:
                        return True
            return False
        except Exception:
            return False

    @staticmethod
    def strip_thinking_tags(text: str) -> str:
        """Remove Qwen3/DeepSeek <think>...</think> reasoning traces from output."""
        if not text:
            return ""
        # Remove enclosed think block
        cleaned = re.sub(r"<think>[\s\S]*?</think>", "", text, flags=re.IGNORECASE)
        # Remove orphan tags if cut off
        cleaned = re.sub(r"</?think>", "", cleaned, flags=re.IGNORECASE)
        return cleaned.strip()

    def generate(
        self,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 0.3,
        max_tokens: int = 2048,
    ) -> Optional[str]:
        """Send generation request to Ollama with timeout and thinking tag cleanup."""
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
            }
        }
        if system:
            payload["system"] = system

        try:
            resp = self.session.post(url, json=payload, timeout=self.timeout)
            if resp.status_code == 200:
                raw_out = resp.json().get("response", "")
                return self.strip_thinking_tags(raw_out)
            else:
                logger.warning(f"Ollama returned HTTP {resp.status_code}: {resp.text[:100]}")
                return None
        except requests.exceptions.Timeout:
            logger.warning(f"Ollama request timed out after {self.timeout}s.")
            return None
        except Exception as e:
            logger.warning(f"Ollama generation failed: {e}")
            return None

    def rewrite_explanation(self, prompt: str, current_explanation: str, concept: str) -> Optional[str]:
        """Rewrite and enhance an explanation using local Qwen3 8B."""
        sys_prompt = "You are a concise, world-class Python educator. Return only the revised explanation text."
        user_prompt = f"""Target Concept: {concept}
Question Prompt:
{prompt}

Current Explanation:
{current_explanation}

Task:
Rewrite this explanation to be crystal-clear, pedagogically rigorous, and directly highlight the mental model.
Do not include extra chatter or headings. Return only the explanation text."""
        return self.generate(user_prompt, system=sys_prompt, temperature=0.2, max_tokens=350)

    def generate_hint(self, prompt: str, correct_answer: Any, concept: str) -> Optional[str]:
        """Generate a progressive, guiding hint that does not give away the answer."""
        sys_prompt = "You are a supportive Python coach. Return only the hint text."
        user_prompt = f"""Target Concept: {concept}
Question:
{prompt}

Correct Answer:
{correct_answer}

Task:
Provide a 1-2 sentence hint that guides the student toward finding the answer themselves without revealing the answer directly.
Return only the hint text."""
        return self.generate(user_prompt, system=sys_prompt, temperature=0.3, max_tokens=450)

    def generate_question_variant(self, item_dict: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Generate a parallel variant of an existing exercise testing the same concept."""
        sys_prompt = "You are an automated Python curriculum variant generator. Return valid JSON only."
        user_prompt = f"""Given this Python curriculum exercise:
{json.dumps(item_dict, indent=2)}

Task:
Create a parallel variation testing the exact same concept ('{item_dict.get('concept')}') and skill ('{item_dict.get('skill')}'), but using different variable names, context, or numbers.
Keep the exact same JSON schema and exercise type ('{item_dict.get('type')}').
Do not change the item ID.
Return ONLY valid JSON with no markdown formatting."""
        raw = self.generate(user_prompt, system=sys_prompt, temperature=0.4, max_tokens=800)
        if not raw:
            return None

        # Clean JSON from response
        try:
            # Strip markdown fences if present
            fence = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", raw)
            json_str = fence.group(1).strip() if fence else raw.strip()
            first = json_str.find("{")
            last = json_str.rfind("}")
            if first != -1 and last != -1:
                json_str = json_str[first : last + 1]
            return json.loads(json_str)
        except Exception as e:
            logger.warning(f"Could not parse variant JSON from Qwen: {e}")
            return None
