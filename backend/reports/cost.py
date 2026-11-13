"""Dollar cost of a model call, in plain code with exact Decimals."""

from decimal import ROUND_HALF_UP, Decimal

# (input, output) US dollars per million tokens. Foundry bills at these rates.
PRICES_PER_MTOK = {
    "claude-opus-5-5": (Decimal(4), Decimal(20)),
    "claude-opus-5-5-fast": (Decimal(8), Decimal(40)),
    "claude-sonnet-5-5": (Decimal(2), Decimal(10)),
    "claude-haiku-5-5": (Decimal("0.10"), Decimal("0.50")),
}
ONE_MILLION = Decimal(1_000_000)
MICRO_DOLLAR = Decimal("0.000001")


def cost_usd(model: str, input_tokens: int, output_tokens: int) -> Decimal:
    """Return the call's cost in dollars, rounded to 6 decimal places.

    A model with no listed price (such as the test fake) costs zero.
    """
    input_price, output_price = PRICES_PER_MTOK.get(model, (Decimal(0), Decimal(0)))
    total = (input_tokens * input_price + output_tokens * output_price) / ONE_MILLION
    return total.quantize(MICRO_DOLLAR, rounding=ROUND_HALF_UP)
