"""The real model client: Claude through Microsoft Foundry."""

import os

from anthropic import AsyncAnthropicFoundry

from .base import LLMClient, LLMResult

DEFAULT_DEPLOYMENT = "claude-opus-5-5-fast"
MAX_TOKENS = 16000


class FoundryLLM(LLMClient):
    """Sends each prompt to a Foundry deployment and returns the reply's text and tokens."""

    def __init__(self, client: AsyncAnthropicFoundry, deployment: str) -> None:
        """Keep the SDK client and the deployment name to send as `model`."""
        self.client = client
        self.deployment = deployment

    async def complete(self, step: str, system: str, prompt: str) -> LLMResult:
        """Send one user prompt and join the reply's text blocks, skipping thinking."""
        message = await self.client.messages.create(
            model=self.deployment,
            system=system,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=MAX_TOKENS,
        )
        text = "".join(block.text for block in message.content if block.type == "text")
        return LLMResult(
            text=text,
            model=message.model,
            input_tokens=message.usage.input_tokens,
            output_tokens=message.usage.output_tokens,
        )


def get_llm_client() -> LLMClient:
    """Build the Foundry client from env: endpoint, API key and deployment name."""
    client = AsyncAnthropicFoundry(
        api_key=os.environ.get("ANTHROPIC_FOUNDRY_API_KEY"),
        base_url=os.environ.get("ANTHROPIC_FOUNDRY_ENDPOINT"),
    )
    deployment = os.environ.get("ANTHROPIC_FOUNDRY_DEPLOYMENT") or DEFAULT_DEPLOYMENT
    return FoundryLLM(client=client, deployment=deployment)
