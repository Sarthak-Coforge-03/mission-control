"""Tests for the Report model's stored fields and defaults."""

import pytest
from reports.models import Report


@pytest.mark.django_db
def test_new_report_gets_pipeline_defaults():
    """A report saved with only the form fields starts empty and waiting for the pipeline."""
    report = Report.objects.create(
        engineer_name="Ana Ruiz",
        station="PROP-2",
        wind_knots=12.5,
        temp_c=9.0,
        fuel_pct=99.1,
        note="Valve 3 chattered during chill-down.",
    )
    report.refresh_from_db()

    assert report.status == Report.Status.PROCESSING
    assert report.verdict == ""
    assert report.subsystem == ""
    assert report.severity == ""
    assert report.violations == []
    assert report.brief_by_minutes is None
    assert not report.injection_flagged
    assert not report.missing_details_flagged
    assert not report.panic_flagged
    assert report.created_at is not None
