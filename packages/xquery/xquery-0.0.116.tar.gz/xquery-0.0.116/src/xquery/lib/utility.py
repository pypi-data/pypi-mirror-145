import json


def get_json(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)


def build_config_str_from_params(server_name: str, database_name: str, **kwargs) -> str:
    config = (
            f'SERVER={server_name};' +
            f'DATABASE={database_name};'
    )
    for key, value in kwargs.items():
        if value is not None:  # UID and PWD cannot be in full_config if is_trusted_connected = 'yes'
            config += f'{key.upper()}={value};'
    return config
