"""Tests for the Briefing model's defaults and its link to a report."""

import pytest
from reports.models import Briefing, Report


@pytest.mark.django_db
def test_new_briefing_is_pending_and_linked_to_its_report():
    """A briefing starts pending with no approver and is reachable as report.briefing."""
    report = Report.objects.create(
        engineer_name="Ana Ruiz",
        station="PROP-2",
        wind_knots=12.5,
        temp_c=9.0,
        fuel_pct=99.1,
        note="Valve 3 chattered during chill-down.",
    )
    Briefing.objects.create(
        report=report, text="Valve 3 chatter; readings in limits.", rounds=1
    )

    briefing = Report.objects.get(pk=report.pk).briefing

    assert briefing.status == Briefing.Status.PENDING
    assert briefing.rounds == 1
    assert briefing.approved_by == ""
    assert briefing.approved_at is None
    assert briefing.created_at is not None
