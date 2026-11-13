"""The one interface every model call goes through."""

from abc import ABC, abstractmethod
from dataclasses import dataclass

from pydantic import BaseModel


@dataclass(frozen=True)
class LLMResult:
    """A model reply: its text, which model produced it, and the tokens it used."""

    text: str
    model: str
    input_tokens: int
    output_tokens: int


class LLMClient(ABC):
    """Base class for model clients. The pipeline only ever talks to this."""

    @abstractmethod
    async def complete(
        self,
        step: str,
        system: str,
        prompt: str,
        schema: type[BaseModel] | None = None,
    ) -> LLMResult:
        """Send one prompt and return the reply.

        `step` is the pipeline step making the call (e.g. "classify"); it labels
        the call for the trace and lets the fake script replies per step.
        With a `schema`, the reply text is asked to be JSON matching it; callers
        still validate it, since a refusal or cut-off reply may not match.
        """
