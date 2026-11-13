"""Tests for sorting a report: parsing the model's reply and the classify call."""

import pytest
from reports.classify import Classification, classify, parse_classification
from reports.llm.fake import FakeLLM
from reports.models import Report, TraceStep


def test_valid_reply_is_parsed():
    """A reply with a known subsystem and severity is used as is."""
    result, fell_back = parse_classification(
        '{"subsystem": "propulsion", "severity": "medium"}'
    )

    assert result.subsystem == Report.Subsystem.PROPULSION
    assert result.severity == Report.Severity.MEDIUM
    assert fell_back is False


@pytest.mark.parametrize(
    "reply",
    [
        "Propulsion, medium severity.",
        '{"subsystem": "engines", "severity": "medium"}',
        '{"subsystem": "propulsion", "severity": "critical"}',
        '{"subsystem": "propulsion"}',
    ],
    ids=["not-json", "unknown-subsystem", "unknown-severity", "missing-field"],
)
def test_bad_reply_falls_back_to_other_and_high(reply):
    """Any reply that doesn't fit the schema becomes other/high, the safe choice."""
    result, fell_back = parse_classification(reply)

    assert result.subsystem == Report.Subsystem.OTHER
    assert result.severity == Report.Severity.HIGH
    assert fell_back is True


async def test_classify_uses_a_good_reply_and_sends_schema_and_report():
    """A good reply is used; the call sends the schema, the station and the note."""
    llm = FakeLLM(
        {"classify": '{"subsystem": "propulsion", "severity": "medium"}'},
        input_tokens=200,
        output_tokens=20,
    )

    result = await classify(llm, station="PROP-2", note="Valve 3 chattered.")

    assert result.classification == Classification(
        subsystem=Report.Subsystem.PROPULSION, severity=Report.Severity.MEDIUM
    )
    assert result.outcome == TraceStep.Outcome.OK
    assert result.llm_result.input_tokens == 200
    assert result.llm_result.output_tokens == 20
    call = llm.calls[0]
    assert call["step"] == "classify"
    assert call["schema"] is Classification
    assert "PROP-2" in call["prompt"]
    assert "Valve 3 chattered." in call["prompt"]


async def test_classify_bad_reply_falls_back_but_keeps_usage():
    """A reply that fails validation gives other/high, and its tokens are still kept."""
    llm = FakeLLM({"classify": "not json"})

    result = await classify(llm, station="PROP-2", note="Valve 3 chattered.")

    assert result.classification.subsystem == Report.Subsystem.OTHER
    assert result.classification.severity == Report.Severity.HIGH
    assert result.outcome == TraceStep.Outcome.FALLBACK
    assert result.llm_result is not None


async def test_classify_failed_call_falls_back_with_error():
    """If the model call raises, the report still gets other/high and the error is kept."""
    llm = FakeLLM({})

    result = await classify(llm, station="PROP-2", note="Valve 3 chattered.")

    assert result.classification.subsystem == Report.Subsystem.OTHER
    assert result.classification.severity == Report.Severity.HIGH
    assert result.outcome == TraceStep.Outcome.ERROR
    assert result.llm_result is None
    assert "classify" in result.error
