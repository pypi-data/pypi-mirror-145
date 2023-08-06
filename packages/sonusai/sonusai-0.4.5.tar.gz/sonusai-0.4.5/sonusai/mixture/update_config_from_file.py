from copy import deepcopy

import yaml

from sonusai import SonusAIError
from sonusai.mixture import update_truth_settings


def update_config_from_file(file_name: str, config: dict) -> dict:
    new_config = deepcopy(config)

    try:
        with open(file=file_name, mode='r') as f:
            given_config = yaml.safe_load(f)
    except Exception as e:
        raise SonusAIError(f'Error loading config from {file_name}: {e}')

    # Use default config as base and overwrite with given config keys as found
    for key in new_config:
        if key in given_config:
            if key != 'truth_settings':
                new_config[key] = given_config[key]

    if 'truth_settings' in given_config:
        new_config['truth_settings'] = deepcopy(given_config['truth_settings'])

    if not isinstance(new_config['truth_settings'], list):
        new_config['truth_settings'] = [new_config['truth_settings']]

    default_ts = deepcopy(config['truth_settings'])
    if not isinstance(default_ts, list):
        default_ts = [default_ts]

    update_truth_settings(new_config['truth_settings'], default_ts)

    required_keys = [
        'class_labels',
        'class_weights_threshold',
        'dither',
        'feature',
        'frame_size',
        'noises',
        'noise_augmentations',
        'num_classes',
        'seed',
        'target_augmentations',
        'targets',
        'truth_settings',
        'truth_mode',
        'truth_reduction_function',
    ]
    for key in required_keys:
        if key not in new_config:
            raise SonusAIError(f"Missing required '{key}' in {file_name}")

    return new_config
