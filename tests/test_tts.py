import pytest, logging
import os, shutil
from allure import feature, story, step
from src.tts import TtsService
from src.models import TextToSpeach


log = logging.getLogger()

@feature('TtsService')
class TestTtsService:

    @story('Init')
    def test_tts_service_init(self, config_tts):
        tts = TtsService(config_tts)

    @story('Process: use_cache=True')
    def test_tts_process_use_cache(self, config_tts):
        shutil.rmtree(os.path.join(config_tts['tts.data_dir'], "audios/"), ignore_errors=True)
        shutil.rmtree(os.path.join(config_tts['tts.data_dir'], "audios_cache/"), ignore_errors=True)
        tts_service = TtsService(config_tts)
        test_en_audio_file_path = tts_service.process('test_en', TextToSpeach(text='Hello world! It is test!', lang='en'))
        assert os.path.isfile(test_en_audio_file_path)
        test_ru_audio_file_path = tts_service.process('test_ru', TextToSpeach(text='Привет мир! Это тест!', lang='ru'))
        assert os.path.isfile(test_ru_audio_file_path)
        
        assert os.path.isdir(os.path.join(config_tts['tts.data_dir'], "audios_cache/"))
        tts_service.providers = {}
        os.remove(test_en_audio_file_path)
        os.remove(test_ru_audio_file_path)
        test_en_audio_file_path = tts_service.process('test_en_2', TextToSpeach(text='Hello world! It is test!', lang='en'))
        assert os.path.isfile(test_en_audio_file_path)
        test_ru_audio_file_path = tts_service.process('test_ru_2', TextToSpeach(text='Привет мир! Это тест!', lang='ru'))
        assert os.path.isfile(test_ru_audio_file_path)
    
    @story('Process: use_cache=False')
    def test_tts_process_use_no_cache(self, config_tts_no_cache):
        shutil.rmtree(os.path.join(config_tts_no_cache['tts.data_dir'], "audios/"), ignore_errors=True)
        shutil.rmtree(os.path.join(config_tts_no_cache['tts.data_dir'], "audios_cache/"), ignore_errors=True)
        tts_service = TtsService(config_tts_no_cache)
        test_en_audio_file_path = tts_service.process('test_en', TextToSpeach(text='Hello world! It is test!', lang='en'))
        assert os.path.isfile(test_en_audio_file_path)
        test_ru_audio_file_path = tts_service.process('test_ru', TextToSpeach(text='Привет мир! Это тест!', lang='ru'))
        assert os.path.isfile(test_ru_audio_file_path)
        assert not os.path.isdir(os.path.join(config_tts_no_cache['tts.data_dir'], "audios_cache/"))