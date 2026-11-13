"""Sorting a report by subsystem and severity: the reply schema and its safe fallback."""

from pydantic import BaseModel, ValidationError

from .models import Report


class Classification(BaseModel):
    """The model's sorting reply. Only the Report choices are accepted."""

    subsystem: Report.Subsystem
    severity: Report.Severity


# Used when the reply can't be trusted: high gets the fastest brief-by time.
FALLBACK = Classification(
    subsystem=Report.Subsystem.OTHER, severity=Report.Severity.HIGH
)


def parse_classification(text: str) -> tuple[Classification, bool]:
    """Parse the model's JSON reply; return it and whether the fallback was used.

    Anything that isn't valid JSON with a known subsystem and severity gives
    the fallback (other, high) instead of an error.
    """
    try:
        return Classification.model_validate_json(text), False
    except ValidationError:
        return FALLBACK, True
