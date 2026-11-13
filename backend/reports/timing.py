"""Brief-by time in plain code: how soon the Flight Director must be briefed."""

from .models import Report

MINUTES_BY_SEVERITY = {
    Report.Severity.HIGH: Report.BriefBy.HIGH,
    Report.Severity.MEDIUM: Report.BriefBy.MEDIUM,
    Report.Severity.LOW: Report.BriefBy.LOW,
}


def brief_by_minutes(severity: str, has_violation: bool) -> Report.BriefBy:
    """Return 5, 15 or 30 minutes for high, medium or low severity.

    Any launch limit violation counts as high. A missing or unknown severity
    also gets the fastest brief, since it is the safe choice.
    """
    if has_violation:
        return Report.BriefBy.HIGH
    return MINUTES_BY_SEVERITY.get(severity, Report.BriefBy.HIGH)
