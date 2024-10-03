import pytest
import logging
from allure import feature, story, step
from src.tts import TtsService
from src.models import TextToSpeach

log = logging.getLogger()

@feature('TtsService')
class TestTtsService:

    @story('Init')
    def test_tts_service_init(self, config_for_tts):
        tts = TtsService(config_for_tts)

    @story('Process')
    def test_tts_service_init(self, config_for_tts):
        tts = TtsService(config_for_tts)
        # audio_file_path = tts.process('test', TextToSpeach(text='Hello world! It is test!', lang='en'))
        # print(audio_file_path)
        audio_file_path = tts.process('test', TextToSpeach(text='Передаю привет Максиму! Тебе пора спать!', lang='ru'))
        print(audio_file_path)