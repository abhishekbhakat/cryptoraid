from unicodedata import decimal
from api_lib.binance_requests import binance_post, binance_get
from configparser import ConfigParser
import hmac, json, hashlib, time, logging

conf = ConfigParser()
conf.read("config.ini")
logging.basicConfig(level=conf["core"]["logging"])
log = logging.getLogger(__name__)


def system_status() -> dict:
    url = conf["binance"]["base_url"] + conf["binance"]["system_status"]
    key = conf["binance"]["api_key"]
    return binance_get(url, key)


def exhange_info(symbol: str) -> dict:
    url = conf["binance"]["base_url"] + conf["binance"]["exchange_info"]
    key = conf["binance"]["api_key"]
    params = {"symbol": symbol}
    return binance_get(url, key, params=params)


def ticker(symbol: str) -> dict:
    url = conf["binance"]["base_url"] + conf["binance"]["ticker"]
    key = conf["binance"]["api_key"]
    params = {"symbol": symbol}
    return float(binance_get(url, key, params=params).get("price"))


def check_balance():
    url = conf["binance"]["base_url"] + conf["binance"]["balances"]
    timeStamp = int(round(time.time() * 1000))
    body = {"timestamp": timeStamp, "type": "SPOT"}
    key = conf["binance"]["api_key"]
    return binance_get(url, key, body)


resp = check_balance()
print(type(resp))
print(json.dumps(resp, indent=4))
