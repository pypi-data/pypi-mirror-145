from enum import Enum
from .errors import SphereTempConversionError


class Material(Enum):
    PEI = 1
    alumina = 2


def get_sample_temp_from_setpoint(setpoint: float, material: Material) -> float:
    if material == Material.PEI:
        return 0.6268 * setpoint + 6.188
    elif material == Material.alumina:
        return 0.818 * setpoint + 3.0607
    else:
        raise SphereTempConversionError('No valid material specified')


def get_setpoint_from_sample_temp(sample_temp: float, material: Material) -> float:
    if material == Material.PEI:
        return (10 * (250 * sample_temp - 1547)) / 1567
    elif material == Material.alumina:
        return (10000 * sample_temp - 30607) / 8180
    else:
        raise SphereTempConversionError('No valid material specified')


def get_max_sample_temp(material: Material) -> float:
    if material == Material.PEI:
        return 140.0
    elif material == Material.alumina:
        return 200.0
    else:
        raise SphereTempConversionError('No valid material specified')


def get_max_setpoint(material: Material) -> float:
    if material == Material.PEI:
        return 210.0
    elif material == Material.alumina:
        return 240.0
    else:
        raise SphereTempConversionError('No valid material specified')
