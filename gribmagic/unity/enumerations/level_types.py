"""Enumerations for level types"""
from enum import Enum


class LevelTypes(Enum):
    """Enumeration of weather models levels type"""

    SINGLE_LEVEL = "single_level"
    MULTI_LEVEL = "multi_level"
    HEIGHT_ABOVE_GROUND = "heightAboveGround"
    ENTIRE_ATMOSPHERE = "entireAtmosphere"
    ISOBARIC_HPA = "isobaricInhPa"
    ISOBARIC_PA = "isobaricInPa"
    SURFACE = "surface"
    SIGMA = "sigma"
    SIGMA_LAYER = "sigmaLayer"
    HYBRID = "hybrid"
    TROPOPAUSE = "tropopause"
