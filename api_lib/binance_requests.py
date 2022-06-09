import requests
import json
import time
import logging

log = logging.getLogger(__name__)


def binance_post(
    url: str, key: str, signature: str, body: dict = {}, params: dict = {}
):
    log.debug("URL: " + url)
    try:
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-MBX-APIKEY": key,
        }
        body["signature"] = signature
        response = requests.request(
            "POST", url, data=body, headers=headers, params=params
        )
        if not response.status_code == 200:
            log.debug("RESPONSE : " + str(response.status_code))
            log.warning("CHECK CONNECTION")
            time.sleep(5)
            return binance_post(url, key, signature, body)
        return response.json()
    except Exception as e:
        log.error("ERROR: " + e)
        time.sleep(1)
        return binance_post(url, key, signature, body)


def binance_get(url: str, key: str, body: dict = {}, params: dict = {}) -> dict:
    log.debug("URL: " + url)
    try:
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-MBX-APIKEY": key,
        }
        response = requests.request(
            "GET", url, headers=headers, data=body, params=params
        )
        if not response.status_code == 200:
            log.debug("RESPONSE : " + str(response.status_code))
            log.warning("CHECK CONNECTION")
            time.sleep(5)
            return binance_get(url, key)
        return response.json()
    except Exception as e:
        log.error("ERROR: " + e)
        time.sleep(1)
        return binance_get(url, key)
