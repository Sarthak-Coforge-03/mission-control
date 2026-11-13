"""Tests for parsing the model's classification reply, with its safe fallback."""

import pytest
from reports.classify import parse_classification
from reports.models import Report


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
