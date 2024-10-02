from typing import Optional
from envyaml import EnvYAML
import os


def load(path: Optional[str]=None):
    if path:
        config = EnvYAML(path)
    elif os.environ.get('TG_CALLS_GATE_CONFIG_PATH'):
        config = EnvYAML(os.environ.get('TG_CALLS_GATE_CONFIG_PATH'))
    else:
        config = EnvYAML('default.config.yaml')
    return config