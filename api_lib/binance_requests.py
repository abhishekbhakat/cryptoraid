import requests
import json
import time
import logging
import hmac, hashlib

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
        if not response.status_code >= 200 and response.status_code < 300:
            log.debug("RESPONSE : " + str(response.status_code))
            log.warning("CHECK CONNECTION")
            time.sleep(5)
            return binance_post(url, key, signature, body)
        return response.json()
    except Exception as e:
        log.error("ERROR: " + e)
        time.sleep(1)
        return binance_post(url, key, signature, body)


def body_to_params(body: dict) -> str:
    params = ""
    for key, value in body.items():
        params += key + "=" + str(value) + "&"
    return params[:-1]


def binance_get(url: str, key: str, body: dict = {}, params: dict = {}) -> dict:
    log.debug("URL: " + url)
    try:
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-MBX-APIKEY": key,
        }
        # convert body to string
        payload = body_to_params(body)
        log.debug("BODY: " + payload)
        signature = hmac.new(
            key.encode(), payload.encode(), hashlib.sha256
        ).hexdigest()
        payload = payload + "&signature=" + signature
        log.debug("PAYLOAD: " + payload)
        input()
        response = requests.request(
            "GET", url, headers=headers, data=payload, params=params
        )
        if not response.status_code >= 200 and response.status_code < 300:
            log.debug("RESPONSE : " + str(response.status_code))
            log.debug("RESPONSE: " + str(response.text))
            log.warning("CHECK CONNECTION")
            time.sleep(5)
            return binance_get(url, key, body, params)
        return response.json()
    except Exception as e:
        log.error("ERROR: " + str(e))
        time.sleep(1)
        return binance_get(url, key, body, params)


# "symbol=LTCBTC&side=BUY&type=LIMIT&timeInForce=GTC&quantity=1&price=0.1&recvWindow=5000&timestamp=1499827319559" | openssl dgst -sha256 -hmac "NhqPtmdSJYdKjVHjA7PZj4Mge3R5YNiP1e3UZjInClVN65XAbvqqM6A7H5fATj0j"
