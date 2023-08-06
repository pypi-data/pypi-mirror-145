from enum import Enum as _Enum
from typing import NamedTuple as _NamedTuple
from ._classes import Number as _Number


class Units(_NamedTuple):
    temp: tuple[str, str] = ("K", "Kelvin")
    speed: tuple[str, str] = ("m/s", "meter/sec")
    api_name: str = "standard"

    time = ("unix", "UTC")
    pressure = "hPa"
    cloudiness = "%"
    precipitation = ("mm", "millimeters")
    degrees = ("°", "degrees (meteorological)")


class StandardUnits:
    STANDARD = Units()
    METRIC = Units(temp=("°C", "Celsius"), api_name="metric")
    IMPERIAL = Units(temp=("°F", "Fahrenheit"), speed=("mph", "miles/hour"), api_name="imperial")


def convert_temp(
    temp: _Number, __from: Units = StandardUnits.STANDARD, __to: Units = StandardUnits.IMPERIAL
) -> _Number:
    """Converts temperature between different units"""
    if __from == __to:
        return temp

    match (__from, __to):
        case (StandardUnits.STANDARD, StandardUnits.METRIC):
            return temp - 273.15
        case (StandardUnits.STANDARD, StandardUnits.IMPERIAL):
            return 1.8 * (temp - 273.15) + 32
        case (StandardUnits.METRIC, StandardUnits.STANDARD):
            return temp + 273.15
        case (StandardUnits.METRIC, StandardUnits.IMPERIAL):
            return 1.8 * temp + 32
        case (StandardUnits.IMPERIAL, StandardUnits.STANDARD):
            return (temp - 32) * 1.8 + 273.15
        case (StandardUnits.IMPERIAL, StandardUnits.METRIC):
            return (temp - 32) * 1.8
        case _:
            raise NotImplementedError(
                f"Conversion between types '{__from.__class__}' and '{__to.__class__}' is not defined"
            )


_MPS_PER_MPH = 0.44704


def convert_speed(
    speed: _Number, __from: Units = StandardUnits.STANDARD, __to: Units = StandardUnits.IMPERIAL
) -> _Number:
    if __from in {StandardUnits.STANDARD, StandardUnits.METRIC} and __to in {
        StandardUnits.STANDARD,
        StandardUnits.METRIC,
    }:
        return speed

    match (__from, __to):
        case (StandardUnits.STANDARD | StandardUnits.METRIC, StandardUnits.IMPERIAL):
            return speed / _MPS_PER_MPH
        case (StandardUnits.IMPERIAL, StandardUnits.STANDARD | StandardUnits.METRIC):
            return _MPS_PER_MPH * speed
        case _:
            raise NotImplementedError(
                f"Conversion between types '{__from.__class__}' and '{__to.__class__}' is not defined"
            )
