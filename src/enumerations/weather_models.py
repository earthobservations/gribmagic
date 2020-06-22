"""Enumerations for weather models"""
from enum import Enum


class WeatherModels(Enum):
    """Enumeration of weather models"""
    ICON_EU = 'icon_eu'
    ICON_GLOBAL = 'icon_global'
    COSMO_DE2 = 'cosmo_de2'
    GFS = 'gfs'
    AROME = 'arome'
    ARPEGE = 'arpege'
    GEOS5 = 'geos_5'