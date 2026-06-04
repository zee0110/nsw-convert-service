"""Unit tests for the pure conversion functions."""
import pytest

from app import conversions
from app.conversions import ConversionError


def test_length_km_to_mi():
    assert conversions.convert_length(1, "km", "mi") == pytest.approx(0.621371, rel=1e-4)


def test_length_roundtrip():
    metres = conversions.convert_length(5, "ft", "m")
    back = conversions.convert_length(metres, "m", "ft")
    assert back == pytest.approx(5.0)


def test_length_unknown_unit():
    with pytest.raises(ConversionError):
        conversions.convert_length(1, "parsec", "m")


def test_mass_kg_to_lb():
    assert conversions.convert_mass(1, "kg", "lb") == pytest.approx(2.20462, rel=1e-4)


def test_temp_c_to_f():
    assert conversions.convert_temperature(100, "C", "F") == pytest.approx(212.0)


def test_temp_f_to_c():
    assert conversions.convert_temperature(32, "F", "C") == pytest.approx(0.0)


def test_temp_c_to_k():
    assert conversions.convert_temperature(0, "C", "K") == pytest.approx(273.15)


def test_temp_unknown():
    with pytest.raises(ConversionError):
        conversions.convert_temperature(1, "X", "C")


def test_currency_aud_to_usd():
    assert conversions.convert_currency(100, "AUD", "USD") == pytest.approx(66.0)


def test_currency_roundtrip():
    usd = conversions.convert_currency(100, "AUD", "USD")
    back = conversions.convert_currency(usd, "USD", "AUD")
    assert back == pytest.approx(100.0)


def test_currency_unknown():
    with pytest.raises(ConversionError):
        conversions.convert_currency(1, "XYZ", "AUD")
