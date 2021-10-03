""" paring yaml configurations"""
from typing import Dict
import os

import pkg_resources
import yaml

from gribmagic.unity.modules.config.constants import KEY_FORECAST_STEPS


def parse_model_config() -> Dict[str, any]:
    """
    parses general model configurations 
    
    Return:
        Dictionary with all required information to download data 
    """
    model_config = \
        os.environ.get("GM_MODEL_CONFIG",
                       pkg_resources.resource_filename("gribmagic.unity.knowledge", "model_config.yml"))
    with open(model_config) as yaml_file:
        model_config = yaml.load(yaml_file, Loader=yaml.FullLoader)
    
    for model in list(model_config.keys()):
        if model == 'dwd_config':
            continue
        for init_time in list(model_config[model][KEY_FORECAST_STEPS].keys()):
            model_config[model][KEY_FORECAST_STEPS][init_time] = \
                [i for ranges in model_config[model][KEY_FORECAST_STEPS][init_time] for i in range(ranges[0], ranges[1], ranges[2]) ]
    return model_config


def parse_model_variables_mapping() -> Dict[str, any]:
    """
    parses model variables to unified variable names mapping 

    Return:
        Dictionary with all variable names mapping
    """
    model_variables_mapping = \
        os.environ.get("GM_MODEL_VARIABLES_MAPPING",
                       pkg_resources.resource_filename("gribmagic.unity.knowledge", "model_variables_mapping.yml"))
    with open(model_variables_mapping) as yaml_file:
        model_variables_mapping = yaml.load(yaml_file, Loader=yaml.FullLoader)
    return model_variables_mapping


def parse_model_variables_levels_mapping() -> Dict[str, any]:
    """
    parses model variables to level type mapping

    Return:
        Dictionary with all variable names mapping
    """
    model_variables_levels_mapping = \
        os.environ.get("GM_MODEL_VARIABLES_LEVELS_MAPPING",
                       pkg_resources.resource_filename("gribmagic.unity.knowledge", "model_variables_levels_mapping.yml"))
    with open(model_variables_levels_mapping) as yaml_file:
        model_variables_level_mapping = yaml.load(yaml_file, Loader=yaml.FullLoader)
    return model_variables_level_mapping
