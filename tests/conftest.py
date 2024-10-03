import pytest
from envyaml import EnvYAML
# import sys

# import logging
# from random import random, randint


# log = logging.getLogger()

@pytest.fixture()
def config_for_tts():
    return EnvYAML('tests/configs/tts.config.yaml')
