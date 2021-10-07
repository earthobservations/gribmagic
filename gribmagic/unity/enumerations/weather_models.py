"""Enumerations for weather models"""
from enum import Enum


class WeatherModels(Enum):
    """Enumeration of weather models"""
    ICON_EU = 'icon_eu'
    ICON_EU_EPS = 'icon_eu_eps'
    ICON_GLOBAL = 'icon_global'
    COSMO_D2 = 'cosmo_d2'
    COSMO_D2_EPS = 'cosmo_d2_eps'
    GFS_025 = 'ncep_gfs_025'
    GFS_050 = 'ncep_gfs_050'
    GFS_100 = 'ncep_gfs_100'
    AROME_METEO_FRANCE = 'arome_meteo_france'
    HARMONIE_KNMI = 'harmonie_knmi'
    ARPEGE = 'arpege'
    GEOS5 = 'geos_5'
