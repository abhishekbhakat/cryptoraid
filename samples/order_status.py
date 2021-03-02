import hmac
import hashlib
import base64
import json
import time
import requests

# Enter your API Key and Secret here. If you don't have one, you can generate it from the website.
key = "XXXX"
secret = "YYYY"

# python3
secret_bytes = bytes(secret, encoding='utf-8')
# python2
secret_bytes = bytes(secret)

# Generating a timestamp.
timeStamp = int(round(time.time() * 1000))

body = {
  "id": "ead19992-43fd-11e8-b027-bb815bcb14ed", # Enter your Order ID here.
  "timestamp": timeStamp
}

json_body = json.dumps(body, separators = (',', ':'))

signature = hmac.new(secret_bytes, json_body.encode(), hashlib.sha256).hexdigest()

url = "https://api.coindcx.com/exchange/v1/orders/status"

headers = {
    'Content-Type': 'application/json',
    'X-AUTH-APIKEY': key,
    'X-AUTH-SIGNATURE': signature
}

response = requests.post(url, data = json_body, headers = headers)
data = response.json()
print(data)