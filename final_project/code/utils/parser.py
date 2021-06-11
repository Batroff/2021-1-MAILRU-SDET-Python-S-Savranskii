from typing import Dict
from re import sub


def parse_config(filepath: str) -> Dict[str, str]:
    settings = {}

    with open(file=filepath, mode='r') as f:
        for line in f.readlines():
            if '=' not in line:
                continue

            key, value = map(lambda x: x.strip(), sub('[\"\']', '', line).split('='))
            settings[str(key)] = str(value)

    return settings
