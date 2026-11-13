"""Tests for FakeLLM, the stand-in model client used by every test."""

import time

import pytest
from reports.llm.base import LLMClient, LLMResult
from reports.llm.fake import FakeLLM


async def test_returns_scripted_reply_with_token_counts():
    """A step's scripted text comes back as an LLMResult with the configured tokens."""
    llm = FakeLLM(
        {"classify": '{"severity": "low"}'}, input_tokens=120, output_tokens=30
    )

    result = await llm.complete("classify", system="Sort it.", prompt="Valve chatter.")

    assert isinstance(llm, LLMClient)
    assert result == LLMResult(
        text='{"severity": "low"}',
        model="fake-model",
        input_tokens=120,
        output_tokens=30,
    )


async def test_list_of_replies_is_returned_in_turn():
    """A list scripts successive calls to the same step, as the draft/review loop needs."""
    llm = FakeLLM({"review": ["needs work", "approved"]})

    first = await llm.complete("review", system="s", prompt="draft 1")
    second = await llm.complete("review", system="s", prompt="draft 2")

    assert [first.text, second.text] == ["needs work", "approved"]


async def test_every_call_is_recorded():
    """Each call's step, system prompt and prompt are kept so tests can inspect them."""
    llm = FakeLLM({"draft": "Briefing text."})

    await llm.complete(
        "draft", system="Write a briefing.", prompt="Feedback: be shorter."
    )

    assert llm.calls == [
        {
            "step": "draft",
            "system": "Write a briefing.",
            "prompt": "Feedback: be shorter.",
        }
    ]


@pytest.mark.parametrize("replies", [{}, {"review": ["only one"]}])
async def test_unscripted_or_used_up_step_raises(replies):
    """Asking for a step with no reply left fails loudly instead of inventing one."""
    llm = FakeLLM(replies)
    if replies:
        await llm.complete("review", system="s", prompt="p")

    with pytest.raises(LookupError, match="review"):
        await llm.complete("review", system="s", prompt="p")


async def test_delay_makes_the_call_wait():
    """A delay makes each call take at least that long, to test concurrency later."""
    llm = FakeLLM({"check_panic": "calm"}, delay=0.05)

    start = time.perf_counter()
    await llm.complete("check_panic", system="s", prompt="p")

    assert time.perf_counter() - start >= 0.05
