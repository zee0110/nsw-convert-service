"""Pure conversion logic — unit conversions and a small fixed currency table.

Kept separate from the web layer so it is trivially unit-testable.
"""

# Length conversions expressed as metres per unit.
LENGTH_TO_METRES = {
    "m": 1.0,
    "km": 1000.0,
    "cm": 0.01,
    "mm": 0.001,
    "mi": 1609.344,
    "ft": 0.3048,
    "in": 0.0254,
    "yd": 0.9144,
}

# Mass conversions expressed as grams per unit.
MASS_TO_GRAMS = {
    "g": 1.0,
    "kg": 1000.0,
    "mg": 0.001,
    "lb": 453.59237,
    "oz": 28.349523125,
    "t": 1_000_000.0,
}

# Illustrative fixed exchange rates relative to AUD (NOT live rates).
AUD_RATES = {
    "AUD": 1.0,
    "USD": 0.66,
    "EUR": 0.61,
    "GBP": 0.52,
    "INR": 55.0,
    "JPY": 99.0,
    "NZD": 1.08,
}


class ConversionError(ValueError):
    """Raised for unknown units or currencies."""


def convert_length(value: float, from_unit: str, to_unit: str) -> float:
    try:
        metres = value * LENGTH_TO_METRES[from_unit]
        return metres / LENGTH_TO_METRES[to_unit]
    except KeyError as e:
        raise ConversionError(f"Unknown length unit: {e.args[0]}") from e


def convert_mass(value: float, from_unit: str, to_unit: str) -> float:
    try:
        grams = value * MASS_TO_GRAMS[from_unit]
        return grams / MASS_TO_GRAMS[to_unit]
    except KeyError as e:
        raise ConversionError(f"Unknown mass unit: {e.args[0]}") from e


def convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    from_unit, to_unit = from_unit.upper(), to_unit.upper()
    # Normalise to Celsius first.
    if from_unit == "C":
        c = value
    elif from_unit == "F":
        c = (value - 32) * 5 / 9
    elif from_unit == "K":
        c = value - 273.15
    else:
        raise ConversionError(f"Unknown temperature unit: {from_unit}")

    if to_unit == "C":
        return c
    if to_unit == "F":
        return c * 9 / 5 + 32
    if to_unit == "K":
        return c + 273.15
    raise ConversionError(f"Unknown temperature unit: {to_unit}")


def convert_currency(value: float, from_cur: str, to_cur: str) -> float:
    from_cur, to_cur = from_cur.upper(), to_cur.upper()
    try:
        aud = value / AUD_RATES[from_cur]
        return aud * AUD_RATES[to_cur]
    except KeyError as e:
        raise ConversionError(f"Unknown currency: {e.args[0]}") from e
