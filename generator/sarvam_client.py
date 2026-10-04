"""
Sarvam AI Client for Codolingo Curriculum Generator.
Provides resilient API calling with exponential backoff, rate limiting, and response parsing.
"""

import json
import logging
import os
import re
import time
from typing import Any, Dict, List, Optional, Tuple

import requests
from dotenv import load_dotenv

# Try importing official SDK
try:
    from sarvamai import SarvamAI
    HAVE_SARVAM_SDK = True
except ImportError:
    HAVE_SARVAM_SDK = False

logger = logging.getLogger("SarvamClient")

class SarvamClient:
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        request_delay: Optional[float] = None,
        max_retries: Optional[int] = None,
        timeout: Optional[float] = None,
    ):
        # Always reload from .env if present
        load_dotenv(override=True)

        self.api_key = api_key or os.getenv("SARVAM_API_KEY", "").strip()
        raw_model = model or os.getenv("SARVAM_MODEL", "sarvam-105b-conversations").strip()
        # Normalize model string
        self.model = raw_model.lower() if raw_model.lower().startswith("sarvam-") else raw_model

        self.request_delay = float(request_delay if request_delay is not None else os.getenv("SARVAM_REQUEST_DELAY", "1.5"))
        self.max_retries = int(max_retries if max_retries is not None else os.getenv("SARVAM_MAX_RETRIES", "4"))
        self.timeout = float(timeout if timeout is not None else os.getenv("SARVAM_TIMEOUT", "180"))

        self.last_request_time: float = 0.0

        # Initialize official SDK client if available
        self.sdk_client: Optional[Any] = None
        if HAVE_SARVAM_SDK and self.api_key:
            try:
                self.sdk_client = SarvamAI(api_subscription_key=self.api_key, timeout=self.timeout)
            except Exception as e:
                logger.warning(f"Could not initialize SarvamAI SDK: {e}. Will use direct HTTP.")

        # Reusable HTTP session for direct REST fallback
        self.http_session = requests.Session()

    def has_api_key(self) -> bool:
        return bool(self.api_key and len(self.api_key) > 5)

    def _apply_rate_limit(self) -> None:
        """Enforce configurable delay between consecutive API requests."""
        if self.request_delay <= 0:
            return
        now = time.time()
        elapsed = now - self.last_request_time
        if elapsed < self.request_delay:
            time.sleep(self.request_delay - elapsed)
        self.last_request_time = time.time()

    def _call_via_sdk(self, messages: List[Dict[str, str]], temperature: float = 0.2, max_tokens: int = 8192) -> str:
        """Execute chat completion using the official SarvamAI SDK."""
        if not self.sdk_client:
            raise RuntimeError("SarvamAI SDK client not initialized")

        response = self.sdk_client.chat.completions(
            messages=messages,
            model=self.model,
            temperature=temperature,
            max_tokens=max_tokens,
        )

        if hasattr(response, "choices") and response.choices:
            choice = response.choices[0]
            if hasattr(choice, "message"):
                msg = choice.message
                content = getattr(msg, "content", None)
                if content:
                    return content
                # If finish_reason is length and content is None
                if getattr(choice, "finish_reason", None) == "length":
                    raise ValueError("Sarvam model token limit reached during reasoning. Increase max_tokens.")
            elif isinstance(choice, dict):
                content = choice.get("message", {}).get("content")
                if content:
                    return content

        raise ValueError("Malformed response format received from SarvamAI SDK")

    def _call_via_http(self, messages: List[Dict[str, str]], temperature: float = 0.2, max_tokens: int = 8192) -> str:
        """Execute chat completion using direct REST API call."""
        url = "https://api.sarvam.ai/v1/chat/completions"
        headers = {
            "api-subscription-key": self.api_key,
            "Content-Type": "application/json",
            "User-Agent": "CodolingoCurriculumGenerator/1.0",
        }
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        resp = self.http_session.post(url, headers=headers, json=payload, timeout=self.timeout)

        # Handle rate limits or temporary server errors
        if resp.status_code == 429:
            retry_after = resp.headers.get("Retry-After")
            wait_time = float(retry_after) if retry_after and retry_after.isdigit() else 5.0
            raise requests.exceptions.HTTPError(f"429 Rate Limited (Retry-After: {wait_time}s)", response=resp)

        resp.raise_for_status()
        data = resp.json()

        choices = data.get("choices", [])
        if choices and "message" in choices[0]:
            return choices[0]["message"].get("content", "")

        raise ValueError("No choices or message content found in Sarvam HTTP response")

    def complete(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.2,
        max_tokens: int = 8192
    ) -> str:
        """
        Send a chat completion request to Sarvam with automatic retries and exponential backoff.
        """
        if not self.has_api_key():
            raise ValueError(
                "SARVAM_API_KEY is not set or empty. "
                "Please add your Sarvam API key to .env file (SARVAM_API_KEY=your_key)."
            )

        attempt = 0
        backoff = 2.0

        while attempt <= self.max_retries:
            attempt += 1
            self._apply_rate_limit()

            try:
                # Primary attempt via SDK if available, otherwise direct HTTP
                if self.sdk_client:
                    try:
                        return self._call_via_sdk(messages, temperature=temperature, max_tokens=max_tokens)
                    except Exception as sdk_err:
                        logger.warning(f"SDK attempt {attempt} failed ({sdk_err}). Falling back to HTTP...")
                        return self._call_via_http(messages, temperature=temperature, max_tokens=max_tokens)
                else:
                    return self._call_via_http(messages, temperature=temperature, max_tokens=max_tokens)

            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as net_err:
                logger.warning(f"[Attempt {attempt}/{self.max_retries}] Network error: {net_err}")
                if attempt > self.max_retries:
                    raise
                time.sleep(backoff)
                backoff *= 2.0

            except requests.exceptions.HTTPError as http_err:
                status = http_err.response.status_code if http_err.response is not None else 0
                logger.warning(f"[Attempt {attempt}/{self.max_retries}] HTTP {status} error: {http_err}")

                if status == 429:
                    # Rate limited: wait longer
                    wait = backoff * 2.0
                    time.sleep(wait)
                    backoff *= 2.0
                elif 500 <= status < 600:
                    time.sleep(backoff)
                    backoff *= 2.0
                else:
                    # Non-retryable client error (e.g. 400 Bad Request, 401 Unauthorized, 403 Forbidden)
                    raise

            except Exception as e:
                logger.warning(f"[Attempt {attempt}/{self.max_retries}] Unexpected error: {e}")
                if attempt > self.max_retries:
                    raise
                time.sleep(backoff)
                backoff *= 2.0

        raise RuntimeError(f"Exceeded max retries ({self.max_retries}) calling Sarvam API")

    @staticmethod
    def extract_json(raw_text: str) -> Any:
        """
        Safely extract and parse JSON from model output, handling markdown code fences,
        arrays [ ... ], objects { ... }, and whitespace.
        """
        if not raw_text or not raw_text.strip():
            raise ValueError("Empty response received from model")

        text = raw_text.strip()

        # Clean trailing commas which frequently appear in LLM JSON outputs
        clean_text = re.sub(r",\s*([\]}])", r"\1", text)

        # 1. Direct parse attempt
        try:
            return json.loads(clean_text, strict=False)
        except json.JSONDecodeError:
            pass

        # 2. Extract from explicit ```json ... ``` code fence first
        json_fence = re.search(r"```json\s*([\s\S]*?)\s*```", text, re.IGNORECASE)
        if json_fence:
            fence_content = re.sub(r",\s*([\]}])", r"\1", json_fence.group(1).strip())
            try:
                return json.loads(fence_content, strict=False)
            except json.JSONDecodeError:
                pass

        # 3. Check for outermost JSON array [ ... ]
        first_bracket = clean_text.find("[")
        last_bracket = clean_text.rfind("]")
        if first_bracket != -1 and last_bracket != -1 and last_bracket > first_bracket:
            first_brace = clean_text.find("{")
            if first_brace == -1 or first_bracket < first_brace:
                arr_substr = clean_text[first_bracket : last_bracket + 1]
                try:
                    return json.loads(arr_substr, strict=False)
                except json.JSONDecodeError:
                    pass

        # 4. Check for outermost JSON object { ... }
        first_brace = clean_text.find("{")
        last_brace = clean_text.rfind("}")
        if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
            obj_substr = clean_text[first_brace : last_brace + 1]
            try:
                return json.loads(obj_substr, strict=False)
            except json.JSONDecodeError:
                pass

        # 5. Extract from any markdown code fence ``` ... ```
        any_fence = re.search(r"```\s*([\s\S]*?)\s*```", text)
        if any_fence:
            fence_content = re.sub(r",\s*([\]}])", r"\1", any_fence.group(1).strip())
            try:
                return json.loads(fence_content, strict=False)
            except json.JSONDecodeError:
                pass

        raise ValueError(f"Could not parse valid JSON from text: {text[:200]}...")
