import requests
import json

def dcx_post(url, body, key, signature):
    headers = {
        'Content-Type': 'application/json',
        'X-AUTH-APIKEY': key,
        'X-AUTH-SIGNATURE': signature
    }

    json_body = json.dumps(body, separators = (',', ':'))
    response = requests.post(url, data = json_body, headers = headers)
    return response.json()


def dcx_get(url):
    response = requests.get(url)
    return response.json()