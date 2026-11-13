"""Tests for the launch limit check: exactly on each limit and just past it."""

import pytest
from reports.limits import evaluate
from reports.models import Report

# Readings comfortably inside every limit; each case changes one of them.
SAFE = {"wind_knots": 10.0, "temp_c": 10.0, "fuel_pct": 99.0}


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("wind_knots", 25.0),
        ("temp_c", 4.0),
        ("fuel_pct", 98.0),
        ("fuel_pct", 100.0),
    ],
)
def test_reading_exactly_on_a_limit_is_go(field, value):
    """A reading exactly on its limit is allowed: go, with no violations."""
    result = evaluate(**{**SAFE, field: value})

    assert result.verdict == Report.Verdict.GO
    assert result.violations == []


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("wind_knots", 25.01),
        ("temp_c", 3.99),
        ("fuel_pct", 97.99),
        ("fuel_pct", 100.01),
    ],
)
def test_reading_just_past_a_limit_is_no_go(field, value):
    """A reading just past its limit makes the verdict no_go with one violation naming it."""
    result = evaluate(**{**SAFE, field: value})

    assert result.verdict == Report.Verdict.NO_GO
    assert len(result.violations) == 1
    assert result.violations[0].startswith(field)


def test_every_broken_limit_is_listed_in_order():
    """With all three readings out of limits, all three violations are listed: wind, temp, fuel."""
    result = evaluate(wind_knots=40.0, temp_c=-2.0, fuel_pct=90.0)

    assert result.verdict == Report.Verdict.NO_GO
    assert [v.split()[0] for v in result.violations] == [
        "wind_knots",
        "temp_c",
        "fuel_pct",
    ]
