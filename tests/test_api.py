# import pytest, logging
# from unittest.mock import Mock, MagicMock
# from allure import feature, story, step
# from src.tts import TtsService
# from src.api import Api
# from src.models import *
# from fastapi.testclient import TestClient

# log = logging.getLogger()

# @feature('Api')
# class TestApi:

#     @story('Init')
#     def test_api_init(self):
#         api = Api(None, None)

#     @story('Helh check')
#     def test_api_health_check(self):
#         api = Api(None, None)
#         client  = TestClient(api.app)
#         response = client.get("/")
#         assert response.status_code == 200
#         assert response.json() == {'health': 'OK'}
#         response = client.get("/health")
#         assert response.status_code == 200
#         assert response.json() == {'health': 'OK'}

#     @story('Call')
#     def test_api_call(self, config_api):
#         tts_service_mock = Mock()
#         method_process_mock = MagicMock(return_value="test.wav")
#         tts_service_mock.process = method_process_mock

#         api = Api(config_api, tts_service_mock)
#         client  = TestClient(api.app)

#         call_request = CallRequest(chat_id=1)
#         response = client.post('/call', json=call_request.model_dump())
#         assert response.status_code == 400
#         assert response.json() == {'detail': "Either 'audio_url' or 'text_to_speech' must be present"}
#         method_process_mock.assert_not_called()

#         call_request = CallRequest(chat_id=1, audio_url='https://test.url.com')
#         response = client.post('/call', json=call_request.model_dump())
#         assert response.status_code == 200
#         result = CallResponse.model_validate(response.json())
#         assert result
#         assert result.audio_file == 'https://test.url.com'
#         method_process_mock.assert_not_called()

#         call_request = CallRequest(chat_id=1, text_to_speech=TextToSpeech(text='Test', lang='en'))
#         response = client.post('/call', json=call_request.model_dump())
#         assert response.status_code == 200
#         result = CallResponse.model_validate(response.json())
#         assert result
#         assert result.audio_file == "test.wav"
#         method_process_mock.assert_called_once_with(result.id, result.call_request.text_to_speech)
    
#     @story('Call with auth')
#     def test_api_call(self, config_api_auth):
#         api = Api(config_api_auth, None)
#         client  = TestClient(api.app)

#         call_request = CallRequest(chat_id=1, audio_url='https://test.url.com')
#         response = client.post('/call', json=call_request.model_dump())
#         assert response.status_code == 401

#         response = client.post('/call', json=call_request.model_dump(), headers={"Authorization": "test"})
#         assert response.status_code == 401

#         response = client.post('/call', json=call_request.model_dump(), headers={"Authorization": "Bearer test"})
#         assert response.status_code == 401
        
#         token = config_api_auth['api.auth_token']
#         response = client.post('/call', json=call_request.model_dump(), headers={"Authorization": f"Bearer {token}"})
#         assert response.status_code == 200
#         result = CallResponse.model_validate(response.json())
#         assert result
#         assert result.audio_file == 'https://test.url.com'