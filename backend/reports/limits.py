"""Launch limit check in plain code. The verdict never comes from a model."""

from dataclasses import dataclass, field

from .models import Report

WIND_MAX_KNOTS = 25
TEMP_MIN_C = 4
FUEL_MIN_PCT = 98
FUEL_MAX_PCT = 100


@dataclass(frozen=True)
class LimitResult:
    """The launch verdict and a readable line for each broken limit."""

    verdict: Report.Verdict
    violations: list[str] = field(default_factory=list)


def evaluate(wind_knots: float, temp_c: float, fuel_pct: float) -> LimitResult:
    """Check the three readings against the launch limits; any violation means no_go.

    Limits are inclusive: a reading exactly on its limit is allowed.
    """
    violations = []
    if wind_knots > WIND_MAX_KNOTS:
        violations.append(
            f"wind_knots {wind_knots:g} is above the {WIND_MAX_KNOTS} max"
        )
    if temp_c < TEMP_MIN_C:
        violations.append(f"temp_c {temp_c:g} is below the {TEMP_MIN_C} min")
    if not FUEL_MIN_PCT <= fuel_pct <= FUEL_MAX_PCT:
        violations.append(
            f"fuel_pct {fuel_pct:g} is outside {FUEL_MIN_PCT}-{FUEL_MAX_PCT}"
        )

    verdict = Report.Verdict.NO_GO if violations else Report.Verdict.GO
    return LimitResult(verdict=verdict, violations=violations)
