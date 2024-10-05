import pytest
import logging
from allure import feature, story, step
from src.models import *

log = logging.getLogger()

@feature('Models')
class TestModels:
   
    @story("Init call models")
    def test_call_models_init(self):
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
        assert call_request.id
        assert call_request.created_at
        assert call_request.audio_url == 'https://test.url.com'
        assert call_request.text_to_speech == text_to_speach
        assert call_request.message_before == {}
        assert call_request.message_after == {}
        assert call_request.send_audio_after_call

        call_response = CallResponse(
            chat_id=1,
            call_request=call_request
        )
        assert call_response.call_request == call_request
        call_response.status = Status.ERROR
        call_response.status_details = 'Test Error'
        assert call_response.status == Status.ERROR
        assert call_response.status_details == 'Test Error'



    @story("Init message models")
    def test_message_models_init(self):
        id = get_id()
        assert id
    
        message_request = MessageRequest(chat_id=1, text='Test')
        assert message_request.text == 'Test'
        assert message_request.chat_id == 1
        assert message_request.id
        assert message_request.created_at

        message_response = MessageResponse(
            message_request = message_request
        )
        assert message_response.message_request == message_request
        message_response.status = Status.ERROR
        message_response.status_details = 'Test Error'
        assert message_response.status == Status.ERROR
        assert message_response.status_details == 'Test Error'