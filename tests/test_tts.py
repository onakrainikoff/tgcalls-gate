import pytest, logging
import os, shutil
from allure import feature, story, step
from src.tts import TtsService
from src.models import TextToSpeech


log = logging.getLogger()

@feature('TtsService')
class TestTtsService:

    @story('Init')
    def test_tts_service_init(self, config_tts):
        tts = TtsService(config_tts)
    
    @story('Process: use_cache=False')
    def test_tts_process_use_no_cache(self, config_tts_no_cache):
        shutil.rmtree(os.path.join(config_tts_no_cache['data_dir'], "tts/audios/"), ignore_errors=True)
        shutil.rmtree(os.path.join(config_tts_no_cache['data_dir'], "tts/audios_cache/"), ignore_errors=True)
        tts_service = TtsService(config_tts_no_cache)
        
        text_to_speech_en = TextToSpeech(text='Hello world! It is test!', lang='en')
        tts_service.process('test_en', text_to_speech_en)
        assert os.path.isfile(text_to_speech_en.audio_file_path)

        text_to_speech_ru = TextToSpeech(text='Привет мир! Это тест!', lang='ru')
        tts_service.process('test_ru', text_to_speech_ru)
        assert os.path.isfile(text_to_speech_ru.audio_file_path)
        
        assert not os.path.isdir(os.path.join(config_tts_no_cache['data_dir'], "tts/audios_cache/"))


    @story('Process: use_cache=True')
    def test_tts_process_use_cache(self, config_tts):
        shutil.rmtree(os.path.join(config_tts['data_dir'], "tts/audios/"), ignore_errors=True)
        shutil.rmtree(os.path.join(config_tts['data_dir'], "tts/audios_cache/"), ignore_errors=True)
        tts_service = TtsService(config_tts)
        
        text_to_speech_en = TextToSpeech(text='Hello world! It is test!', lang='en')
        tts_service.process('test_en', text_to_speech_en)
        assert os.path.isfile(text_to_speech_en.audio_file_path)
        text_to_speech_ru = TextToSpeech(text='Привет мир! Это тест!', lang='ru')
        tts_service.process('test_ru', text_to_speech_ru)
        assert os.path.isfile(text_to_speech_ru.audio_file_path)

        assert os.path.isdir(os.path.join(config_tts['data_dir'], "tts/audios_cache/"))
        tts_service.providers = {}
        os.remove(text_to_speech_en.audio_file_path)
        os.remove(text_to_speech_ru.audio_file_path)
        text_to_speech_en2 = TextToSpeech(text='Hello world! It is test!', lang='en')
        tts_service.process('test_en_2', text_to_speech_en2)
        assert os.path.isfile(text_to_speech_en2.audio_file_path)
        text_to_speech_ru2 = TextToSpeech(text='Привет мир! Это тест!', lang='ru')
        tts_service.process('test_ru_2', text_to_speech_ru2)
        assert os.path.isfile(text_to_speech_ru2.audio_file_path)

    @story('Process: Unsupported lang')
    @pytest.mark.xfail(raises=RuntimeError)
    def test_tts_process_unsupported_lang(self, config_tts):
        tts_service = TtsService(config_tts)
        text_to_speech_unsupported_lang = TextToSpeech(text='Hello world! It is test!', lang='unsupported_lang')
        tts_service.process('test_unsupported_lang', text_to_speech_unsupported_lang)