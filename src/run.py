
import os
import argparse
from typing import Optional
from envyaml import EnvYAML
from api import Api

def load_config():
    parser = argparse.ArgumentParser(description="TgCalls-Gate")
    parser.add_argument('-c','--config', metavar='', type=str, default=None, help='path to config.yaml file')
    args = parser.parse_args()
    config_path = args.config
    if config_path:
        config = EnvYAML(config_path)
    elif os.environ.get('TG_CALLS_GATE_CONFIG_PATH'):
        config = EnvYAML(os.environ.get('TG_CALLS_GATE_CONFIG_PATH'))
    else:
        config = EnvYAML('default.config.yaml')
    return config

if __name__ == "__main__":
    config = load_config()
    api = Api(config)
    api.run()
    