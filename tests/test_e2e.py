import pytest, logging, requests
import os, shutil
from allure import feature, story, step

API_URL = 'http://localhost'
log = logging.getLogger()


def test_api_get_health():
    url = f"{API_URL}/health"
    headers = {'Content-Type': 'application/json'}  
    response = requests.get(url, headers=headers)
    log.info(f"response: starus={response.status_code}, body={response.text}")
    assert response.status_code == 200
    


def test_api_post_call():
    pass

def test_api_post_message():
    pass

def test_api_post_call_test():
    url = f"{API_URL}/call/test/"
    headers = {'Content-Type': 'application/json'}  
    response = requests.post(url, headers=headers, data={})
    log.info(f"response: starus={response.status_code}, body={response.text}")
    assert response.status_code == 200

def test_tg_private_chat():
    pass