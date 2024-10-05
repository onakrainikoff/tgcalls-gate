import pytest, logging
from envyaml import EnvYAML

log = logging.getLogger()

@pytest.fixture()
def config_api():
    return EnvYAML('tests/resources/test_api.config.yaml')
@pytest.fixture()
def config_api_auth():
    return EnvYAML('tests/resources/test_api_auth.config.yaml')

@pytest.fixture()
def config_tts_no_cache():
    return EnvYAML('tests/resources/test_tts_no_cache.config.yaml')

@pytest.fixture()
def config_tts():
    return EnvYAML('tests/resources/test_tts.config.yaml')