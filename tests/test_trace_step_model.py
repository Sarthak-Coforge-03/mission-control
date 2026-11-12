"""Tests for TraceStep rows and a report's total cost."""

from decimal import Decimal

import pytest
from reports.models import Report, TraceStep


def make_report() -> Report:
    """Create a report with valid form fields for trace tests."""
    return Report.objects.create(
        engineer_name="Ana Ruiz",
        station="PROP-2",
        wind_knots=30.0,
        temp_c=9.0,
        fuel_pct=99.1,
        note="Valve 3 chattered during chill-down.",
    )


@pytest.mark.django_db
def test_steps_come_back_in_order_with_code_step_defaults():
    """Steps are returned by their order, and a code step defaults to no tokens and no cost."""
    report = make_report()
    TraceStep.objects.create(report=report, order=2, step=TraceStep.Step.CLASSIFY)
    TraceStep.objects.create(report=report, order=1, step=TraceStep.Step.LIMITS)

    steps = list(report.trace_steps.all())

    assert [s.step for s in steps] == [TraceStep.Step.LIMITS, TraceStep.Step.CLASSIFY]
    limits = steps[0]
    assert limits.input_tokens == 0
    assert limits.output_tokens == 0
    assert limits.cost_usd == Decimal(0)
    assert limits.outcome == TraceStep.Outcome.OK
    assert limits.round is None
    assert limits.output == {}


@pytest.mark.django_db
def test_total_cost_is_exact_sum_of_step_costs():
    """Total cost adds step costs as Decimals with no float rounding error."""
    report = make_report()
    TraceStep.objects.create(
        report=report,
        order=1,
        step=TraceStep.Step.CLASSIFY,
        cost_usd=Decimal("0.000123"),
    )
    TraceStep.objects.create(
        report=report,
        order=2,
        step=TraceStep.Step.DRAFT,
        round=1,
        cost_usd=Decimal("0.000456"),
    )

    assert report.total_cost_usd() == Decimal("0.000579")


@pytest.mark.django_db
def test_total_cost_is_zero_without_steps():
    """A report with no trace steps costs nothing."""
    assert make_report().total_cost_usd() == Decimal(0)
