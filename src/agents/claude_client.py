from __future__ import annotations

import json
import logging

LOGGER = logging.getLogger(__name__)


class ClaudeClient:
    def __init__(self, api_key: str, model: str, max_tokens: int, temperature: float) -> None:
        self.api_key = api_key
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self._client = None

        if api_key:
            try:
                from anthropic import Anthropic
                self._client = Anthropic(api_key=api_key)
            except Exception as exc:
                LOGGER.warning("Failed to initialize Anthropic client: %s", exc)

    def is_available(self) -> bool:
        return self._client is not None

    def _extract_balanced_json(self, text: str) -> str:
        start = text.find("{")
        if start == -1:
            return ""

        depth = 0
        in_string = False
        escape = False

        for i in range(start, len(text)):
            ch = text[i]

            if escape:
                escape = False
                continue

            if ch == "\\":
                escape = True
                continue

            if ch == '"':
                in_string = not in_string
                continue

            if not in_string:
                if ch == "{":
                    depth += 1
                elif ch == "}":
                    depth -= 1
                    if depth == 0:
                        return text[start:i + 1]

        return ""

    def _extract_json(self, raw_text: str) -> dict[str, object]:
        text = raw_text.strip()

        # 1. direct parse
        try:
            return json.loads(text)
        except Exception:
            pass

        # 2. remove markdown fences if present
        if text.startswith("```json"):
            text = text.replace("```json", "", 1).strip()
        if text.startswith("```"):
            text = text.replace("```", "", 1).strip()
        if text.endswith("```"):
            text = text[:-3].strip()

        try:
            return json.loads(text)
        except Exception:
            pass

        # 3. balanced JSON extraction
        candidate = self._extract_balanced_json(text)
        if candidate:
            try:
                return json.loads(candidate)
            except Exception:
                LOGGER.warning("Claude returned malformed JSON candidate: %s", candidate[:500])

        LOGGER.warning("Claude returned non-JSON output: %s", raw_text[:500])
        return {}

    def complete_json(self, system_prompt: str, user_prompt: str) -> dict[str, object]:
        if not self._client:
            return {}

        message = self._client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )

        text_chunks = []
        for block in message.content:
            if getattr(block, "type", "") == "text":
                text_chunks.append(block.text)

        raw_text = "\n".join(text_chunks).strip()
        return self._extract_json(raw_text)