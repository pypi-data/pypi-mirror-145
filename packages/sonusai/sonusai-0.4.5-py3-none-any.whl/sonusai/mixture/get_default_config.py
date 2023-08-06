import yaml

import sonusai


def get_default_config() -> dict:
    try:
        with open(file=sonusai.mixture.default_config, mode='r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        raise sonusai.SonusAIError(f'Error loading default config: {e}')
