"""Enumerations for weather models"""
from enum import Enum


class WeatherModels(Enum):
    """Enumeration of weather models"""
    ICON_EU = 'icon_eu'
    ICON_GLOBAL = 'icon_global'
    COSMO_D2 = 'cosmo_d2'
    GFS = 'gfs'
    AROME_METEO_FRANCE = 'arome_meteo_france'
    ARPEGE = 'arpege'
    GEOS5 = 'geos_5'
