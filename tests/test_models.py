import pytest
import logging
from allure import feature, story, step
from src.models import *

log = logging.getLogger()

@feature('Models')
class TestModels:
   
    @story("Init call models")
    def test_call_models_init(self):
        with step('Check id generation'):
            id = get_id()
            assert id
        with step('Check TextToSpeech'):
            text_to_speach = TextToSpeech(text='Test', lang='en')
            assert text_to_speach.text == 'Test'
            assert text_to_speach.lang == 'en'    
        with step('Check CallContent'):
            content = CallContent(
                audio_url='https://test.url.com',
                text_to_speech=text_to_speach,
                message_before=MessageContent(text='Text before'),
                message_after=MessageContent(text='Text after')
            )
            assert content.audio_url == 'https://test.url.com'
            assert content.text_to_speech == text_to_speach
            assert content.message_before.text == 'Text before'
            assert content.message_after.text == 'Text after'
            assert content.send_audio_after_call
        with step('Check CallEntity'):
            entity = CallEntity(
                chat_id=1,
                content=content
            )
            assert entity.chat_id == 1
            assert entity.id
            assert entity.created_at
            assert entity.content == content
            entity.status = Status.ERROR
            entity.status_details = 'Test Error'
            assert entity.status == Status.ERROR
            assert entity.status_details == 'Test Error'



    @story("Init message models")
    def test_message_models_init(self):
        with step('Check id generation'):
            id = get_id()
            assert id
        with step('Check id MessageContent'):
            content = MessageContent(chat_id=1, text='Test')
            assert content.text == 'Test'
        with step('Check id MessageEntity'):
            entity = MessageEntity(
                chat_id=1,
                content = content
            )
            assert entity.chat_id == 1
            assert entity.id
            assert entity.created_at
            assert entity.content == content
            entity.status = Status.ERROR
            entity.status_details = 'Test Error'
            assert entity.status == Status.ERROR
            assert entity.status_details == 'Test Error'