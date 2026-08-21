"""Unified LLM router.

Free-first policy:
  1. DeepSeek (deepseek-chat) for heavy reasoning — used everywhere by default
  2. Groq / Gemini free tiers as fallback or fast path
  3. Anthropic optional

All agents call `llm.complete()` / `llm.structured()` — never provider SDKs directly.
"""
from __future__ import annotations

import json
import re
from typing import Any

from app.core.config import settings


class LLMError(RuntimeError):
    pass


def _extract_json(text: str) -> dict | list:
    """Best-effort extraction of a JSON payload from a model response."""
    text = text.strip()
    fence = re.search(r"```(?:json)?\s*(.*?)```", text, re.DOTALL)
    if fence:
        text = fence.group(1).strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end > start:
            try:
                return json.loads(text[start : end + 1])
            except json.JSONDecodeError:
                pass
        start = text.find("[")
        end = text.rfind("]")
        if start != -1 and end > start:
            try:
                return json.loads(text[start : end + 1])
            except json.JSONDecodeError:
                pass
    raise LLMError(f"Could not parse JSON from model output: {text[:200]}")


class DeepSeekProvider:
    def __init__(self):
        import openai

        self._client = openai.OpenAI(
            api_key=settings.deepseek_api_key,
            base_url=settings.deepseek_base_url,
        )

    @property
    def ready(self) -> bool:
        return bool(settings.deepseek_api_key)

    def complete(self, prompt: str, system: str, temperature: float = 0.3) -> str:
        resp = self._client.chat.completions.create(
            model=settings.deepseek_model_id,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
            temperature=temperature,
        )
        return resp.choices[0].message.content


class GroqProvider:
    def __init__(self):
        from groq import Groq

        self._client = Groq(api_key=settings.groq_api_key)

    @property
    def ready(self) -> bool:
        return bool(settings.groq_api_key)

    def complete(self, prompt: str, system: str, temperature: float = 0.3) -> str:
        resp = self._client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
            temperature=temperature,
        )
        return resp.choices[0].message.content


class GeminiProvider:
    def __init__(self):
        import google.generativeai as genai

        genai.configure(api_key=settings.gemini_api_key)
        self._model = genai.GenerativeModel("gemini-1.5-flash")

    @property
    def ready(self) -> bool:
        return bool(settings.gemini_api_key)

    def complete(self, prompt: str, system: str, temperature: float = 0.3) -> str:
        resp = self._model.generate_content(f"{system}\n\n{prompt}")
        return resp.text


class LLMRouter:
    def __init__(self):
        self._providers = []
        for p in (DeepSeekProvider, GroqProvider, GeminiProvider):
            try:
                inst = p()
                if inst.ready:
                    self._providers.append(inst)
            except Exception:
                continue

    @property
    def ready(self) -> bool:
        return len(self._providers) > 0

    def complete(self, prompt: str, system: str = "", temperature: float = 0.3) -> str:
        if not self._providers:
            raise LLMError("No LLM provider configured")
        for provider in self._providers:
            try:
                return provider.complete(prompt, system, temperature)
            except Exception:
                continue
        raise LLMError("All LLM providers failed")

    def structured(
        self, prompt: str, system: str = "", temperature: float = 0.1
    ) -> dict | list:
        system = system or "You return strict JSON only. No prose, no markdown."
        raw = self.complete(prompt, system, temperature)
        return _extract_json(raw)


llm = LLMRouter()