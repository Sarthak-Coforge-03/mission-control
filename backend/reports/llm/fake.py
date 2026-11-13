"""A scripted stand-in for the model, so tests need no network and no API key."""

import asyncio

from pydantic import BaseModel

from .base import LLMClient, LLMResult


class FakeLLM(LLMClient):
    """Returns scripted replies per step and records every call it receives."""

    def __init__(
        self,
        replies: dict[str, str | list[str]],
        delay: float = 0.0,
        input_tokens: int = 100,
        output_tokens: int = 50,
        model: str = "fake-model",
    ) -> None:
        """Script replies per step; a list gives successive replies for that step."""
        self._replies = {
            step: list(reply) if isinstance(reply, list) else [reply]
            for step, reply in replies.items()
        }
        self._repeat = {
            step for step, reply in replies.items() if isinstance(reply, str)
        }
        self.delay = delay
        self.input_tokens = input_tokens
        self.output_tokens = output_tokens
        self.model = model
        self.calls: list[dict] = []

    async def complete(
        self,
        step: str,
        system: str,
        prompt: str,
        schema: type[BaseModel] | None = None,
    ) -> LLMResult:
        """Record the call, wait `delay` seconds, then return the next scripted reply.

        The schema is recorded but not enforced, so tests can script a bad reply.
        """
        self.calls.append(
            {"step": step, "system": system, "prompt": prompt, "schema": schema}
        )
        await asyncio.sleep(self.delay)

        queue = self._replies.get(step)
        if not queue:
            raise LookupError(f"FakeLLM has no reply scripted for step {step!r}")
        text = queue[0] if step in self._repeat else queue.pop(0)

        return LLMResult(
            text=text,
            model=self.model,
            input_tokens=self.input_tokens,
            output_tokens=self.output_tokens,
        )
