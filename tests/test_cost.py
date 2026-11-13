"""Tests for the dollar cost of a model call, computed in plain code."""

from decimal import Decimal

from reports.cost import cost_usd


def test_opus_cost_uses_per_million_token_prices():
    """Opus 5.5 at $4 in / $20 out per million: 1,000 in + 500 out costs $0.014."""
    assert cost_usd("claude-opus-5-5", 1_000, 500) == Decimal("0.014000")


def test_fast_deployment_costs_double():
    """The fast deployment is billed at $8 in / $40 out, twice the normal rate."""
    assert cost_usd("claude-opus-5-5-fast", 1_000, 500) == Decimal("0.028000")


def test_unknown_model_costs_nothing():
    """A model with no price, like the fake, costs zero instead of crashing."""
    assert cost_usd("fake-model", 1_000, 500) == Decimal(0)


def test_cost_is_rounded_to_six_decimal_places():
    """7 Haiku input tokens cost $0.0000007, which rounds half up to $0.000001."""
    result = cost_usd("claude-haiku-5-5", 7, 0)

    assert result == Decimal("0.000001")
    assert result.as_tuple().exponent == -6
