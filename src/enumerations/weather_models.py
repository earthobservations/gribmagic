"""Enumerations for weather models"""
from enum import Enum


class WeatherModels(Enum):
    """Enumeration of weather models"""
    ICON_EU = 'icon_eu'
    ICON_EU_EPS = 'icon_eu_eps'
    ICON_GLOBAL = 'icon_global'
    COSMO_D2 = 'cosmo_d2'
    COSMO_D2_EPS = 'cosmo_d2'
    GFS_025 = 'ncep_gfs_025'
    AROME_METEO_FRANCE = 'arome_meteo_france'
    HARMONIE_KNMI = 'harmonie_knmi'
    ARPEGE = 'arpege'
    GEOS5 = 'geos_5'
