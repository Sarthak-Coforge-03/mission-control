"""Tests for FoundryLLM, using a stub SDK client so no network or key is needed."""

from types import SimpleNamespace

from anthropic import AsyncAnthropicFoundry, transform_schema
from pydantic import BaseModel
from reports.llm.base import LLMClient, LLMResult
from reports.llm.foundry import FoundryLLM, get_llm_client


class Reply(BaseModel):
    """A tiny reply schema used to test structured output."""

    answer: str


class StubMessages:
    """Stands in for `client.messages`: records the call and returns a canned reply."""

    def __init__(self, reply):
        """Keep the reply to return and an empty list of received calls."""
        self.reply = reply
        self.calls = []

    async def create(self, **kwargs):
        """Record the keyword arguments and return the canned reply."""
        self.calls.append(kwargs)
        return self.reply


def make_reply():
    """Build a reply shaped like the SDK's: a thinking block, two text blocks, usage."""
    return SimpleNamespace(
        model="claude-opus-5-5",
        content=[
            SimpleNamespace(type="thinking", thinking="Let me sort this."),
            SimpleNamespace(type="text", text='{"severity": '),
            SimpleNamespace(type="text", text='"high"}'),
        ],
        usage=SimpleNamespace(input_tokens=321, output_tokens=45),
    )


async def test_complete_sends_prompt_and_returns_text_and_usage():
    """The deployment, system and prompt are sent; only text blocks come back, with usage tokens."""
    messages = StubMessages(make_reply())
    llm = FoundryLLM(
        client=SimpleNamespace(messages=messages), deployment="my-deployment"
    )

    result = await llm.complete("classify", system="Sort it.", prompt="Valve chatter.")

    assert isinstance(llm, LLMClient)
    assert messages.calls == [
        {
            "model": "my-deployment",
            "system": "Sort it.",
            "messages": [{"role": "user", "content": "Valve chatter."}],
            "max_tokens": 16000,
        }
    ]
    assert result == LLMResult(
        text='{"severity": "high"}',
        model="claude-opus-5-5",
        input_tokens=321,
        output_tokens=45,
    )


async def test_schema_is_sent_as_structured_output_format():
    """With a schema, the call asks for JSON output matching it, in the API's format."""
    messages = StubMessages(make_reply())
    llm = FoundryLLM(client=SimpleNamespace(messages=messages), deployment="d")

    await llm.complete("classify", system="s", prompt="p", schema=Reply)

    assert messages.calls[0]["output_config"] == {
        "format": {"type": "json_schema", "schema": transform_schema(Reply)}
    }


def test_get_llm_client_builds_foundry_client_from_env(monkeypatch):
    """The factory reads endpoint, key and deployment from env without calling out."""
    monkeypatch.setenv("ANTHROPIC_FOUNDRY_ENDPOINT", "https://example.test/anthropic")
    monkeypatch.setenv("ANTHROPIC_FOUNDRY_API_KEY", "test-key")
    monkeypatch.setenv("ANTHROPIC_FOUNDRY_DEPLOYMENT", "my-deployment")

    llm = get_llm_client()

    assert isinstance(llm, FoundryLLM)
    assert isinstance(llm.client, AsyncAnthropicFoundry)
    assert llm.client.api_key == "test-key"
    assert str(llm.client.base_url).startswith("https://example.test/anthropic")
    assert llm.deployment == "my-deployment"


def test_get_llm_client_defaults_to_fast_deployment(monkeypatch):
    """With no deployment set, the factory uses the fast Opus deployment."""
    monkeypatch.setenv("ANTHROPIC_FOUNDRY_ENDPOINT", "https://example.test/anthropic")
    monkeypatch.setenv("ANTHROPIC_FOUNDRY_API_KEY", "test-key")
    monkeypatch.delenv("ANTHROPIC_FOUNDRY_DEPLOYMENT", raising=False)

    assert get_llm_client().deployment == "claude-opus-5-5-fast"
