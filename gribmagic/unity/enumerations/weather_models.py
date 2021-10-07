"""Enumerations for weather models"""
from enum import Enum


class WeatherModels(Enum):
    """Enumeration of weather models"""

    DWD_ICON_EU = "dwd-icon-eu"
    DWD_ICON_EU_EPS = "dwd-icon-eu-eps"
    DWD_ICON_GLOBAL = "dwd-icon-global"
    DWD_COSMO_D2 = "dwd-cosmo-d2"
    DWD_COSMO_D2_EPS = "dwd-cosmo-d2-eps"
    NCEP_GFS_025 = "ncep-gfs-025"
    NCEP_GFS_050 = "ncep-gfs-050"
    NCEP_GFS_100 = "ncep-gfs-100"
    METEO_FRANCE_AROME = "meteo-france-arome"
    KNMI_HARMONIE = "knmi-harmonie"
    ARPEGE = "arpege"
    GEOS5 = "geos_5"

    # For testing purposes.
    UNKNOWN = "unknown"
