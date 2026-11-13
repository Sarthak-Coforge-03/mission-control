"""Tests for the brief-by time: it follows severity, and any violation counts as high."""

import pytest
from reports.models import Report
from reports.timing import brief_by_minutes


@pytest.mark.parametrize(
    ("severity", "minutes"),
    [
        (Report.Severity.HIGH, 5),
        (Report.Severity.MEDIUM, 15),
        (Report.Severity.LOW, 30),
    ],
)
def test_time_follows_severity_without_violation(severity, minutes):
    """With readings in limits, high, medium and low map to 5, 15 and 30 minutes."""
    assert brief_by_minutes(severity, has_violation=False) == minutes


@pytest.mark.parametrize(
    "severity", [Report.Severity.LOW, Report.Severity.MEDIUM, Report.Severity.HIGH]
)
def test_any_violation_counts_as_high(severity):
    """A limit violation forces the 5-minute brief, whatever severity the model gave."""
    assert brief_by_minutes(severity, has_violation=True) == Report.BriefBy.HIGH


@pytest.mark.parametrize("severity", ["", "critical"])
def test_missing_or_unknown_severity_is_treated_as_high(severity):
    """A report with no valid severity gets the safest, fastest brief: 5 minutes."""
    assert brief_by_minutes(severity, has_violation=False) == Report.BriefBy.HIGH
