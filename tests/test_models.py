import pytest
import logging
from allure import feature, story, step
from src.models import *

log = logging.getLogger()

@feature('Models')
class TestModels:
   
    @story("Init")
    def test_models_init(self):
        id = get_id()
        assert id
        
        text_to_speach = TextToSpeech(text='Test', lang='en')
        assert text_to_speach.text == 'Test'
        assert text_to_speach.lang == 'en'

        call_request = CallRequest(
            chat_id=1,
            audio_url='https://test.url.com',
            text_to_speech=text_to_speach,
            message_before={},
            message_after={}
        )
        assert call_request.chat_id == 1
        assert call_request.audio_url == 'https://test.url.com'
        assert call_request.text_to_speech == text_to_speach
        assert call_request.message_before == {}
        assert call_request.message_after == {}
        assert call_request.send_audio_after_call

        call = Call(
            call_request=call_request
        )
        assert call.id
        assert call.created_at
        assert call.call_request == call_request
        
        call.result = CallResult.ERROR
        call.result_details = 'Test Error'
        assert call.result == CallResult.ERROR
        assert call.result_details == 'Test Error'