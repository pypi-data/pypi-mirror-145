from sonusai.mixture import get_default_config
from sonusai.mixture import update_config_from_file


def get_config_from_file(config_file: str) -> dict:
    return update_config_from_file(file_name=config_file, config=get_default_config())
