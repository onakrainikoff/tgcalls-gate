import pytest
from envyaml import EnvYAML
# import sys

# import logging
# from random import random, randint


# log = logging.getLogger()

@pytest.fixture()
def config_tts():
    return EnvYAML('tests/configs/tts.config.yaml')

@pytest.fixture()
def config_tts_no_cache():
    return EnvYAML('tests/configs/tts_no_cache.config.yaml')