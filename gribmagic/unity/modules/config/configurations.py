""" provides parsed configurations"""

from gribmagic.unity.modules.config.parse_configurations import parse_model_config, \
    parse_model_variables_mapping, parse_model_variables_levels_mapping


MODEL_CONFIG = parse_model_config()
MODEL_VARIABLES_MAPPING = parse_model_variables_mapping()
MODEL_VARIABLES_LEVELS_MAPPING = parse_model_variables_levels_mapping()
