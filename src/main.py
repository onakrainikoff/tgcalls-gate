
import logging.config
import os, argparse, logging, yaml
from typing import Optional
from envyaml import EnvYAML
from api import Api

log = logging.getLogger()

def get_config():
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

def setup_logging(config:EnvYAML):
    if config.get('logging'):
        logging.config.dictConfig(config['logging'])

def get_tts(config:EnvYAML):
    pass

def get_tg_calls(config:EnvYAML):
    pass

def main():
    config = get_config()
    setup_logging(config)
    log.info("Starting TgCalls-Gate")
    api = Api(config)
    api.run()
    
if __name__ == "__main__":
    main()
