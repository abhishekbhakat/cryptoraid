import requests
import json
import time
import logging

log = logging.getLogger(__name__)


def dcx_post(url: str, key: str, signature: str, json_body: dict = {}) -> dict:
    try:
        headers = {
            "Content-Type": "application/json",
            "X-MBX-APIKEY": key,
            "X-AUTH-SIGNATURE": signature,
        }
        response = requests.post(url, data=json_body, headers=headers)
        if not response.status_code == 200:
            print("CHECK CONNECTION")
            time.sleep(5)
            return dcx_post(url, key, signature, json_body)
        return response.json()
    except Exception as e:
        log.error(e)
        time.sleep(1)
        return dcx_post(url, key, signature, json_body)


def dcx_get(url: str) -> dict:
    try:
        response = requests.get(url)
        return response.json()
    except:
        time.sleep(1)
        return dcx_get(url)
