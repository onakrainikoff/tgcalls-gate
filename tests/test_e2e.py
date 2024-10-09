import pytest, logging, requests
import os, shutil, json
from allure import feature, story, step

API_URL = 'http://localhost'
log = logging.getLogger()


def test_api_get_health():
    url = f"{API_URL}/health"
    headers = {'Content-Type': 'application/json'}  
    response = requests.get(url, headers=headers)
    log.info(f"response: status={response.status_code}, body={response.text}")
    assert response.status_code == 200
    


def test_api_post_call():
    chat_id = int(os.environ.get('TEST_CHAT_ID'))
    api_auth_token = os.environ.get('API_AUTH_TOKEN', '')
    url = f"{API_URL}/call/{chat_id}"
    data = json.loads(
    """
        {
            "audio_url": "https://download.samplelib.com/mp3/sample-15s.mp3"
        }
    """
    )
    headers = {'Content-Type': 'application/json', 'Authorization': f"Bearer {api_auth_token}"}
    response = requests.post(url, headers=headers, json=data)
    log.info(f"response: status={response.status_code}, body={response.text}")
    assert response.status_code == 200

def test_api_post_message():
    chat_id = int(os.environ.get('TEST_CHAT_ID'))
    api_auth_token = os.environ.get('API_AUTH_TOKEN', '')
    url = f"{API_URL}/message/{chat_id}"
    data = json.loads(
    """
        {
            "text": "Test text",
            "photo_url": "https://www.kasandbox.org/programming-images/avatars/marcimus-orange.png"
        }
    """
    )
    headers = {'Content-Type': 'application/json', 'Authorization': f"Bearer {api_auth_token}"}
    response = requests.post(url, headers=headers, json=data)
    log.info(f"response: status={response.status_code}, body={response.text}")
    assert response.status_code == 200


def test_api_post_call_test():
    chat_id = int(os.environ.get('TEST_CHAT_ID'))
    api_auth_token = os.environ.get('API_AUTH_TOKEN', '')
    url = f"{API_URL}/call/test/{chat_id}"
    headers = {'Content-Type': 'application/json', 'Authorization': f"Bearer {api_auth_token}"}
    response = requests.post(url, headers=headers)
    log.info(f"response: status={response.status_code}, body={response.text}")
    assert response.status_code == 200

def test_tg_private_chat():
    pass