from api_lib.binance_requests import binance_post, binance_get
from configparser import ConfigParser
import hmac, json, hashlib, time, logging

conf = ConfigParser()
conf.read('config.ini')
logging.basicConfig(level=conf['core']['logging'])
log = logging.getLogger(__name__)

def system_status():
    url = conf['binance']['base_url'] + conf['binance']['system_status']
    key = conf['binance']['api_key']
    return binance_get(url, key)


system_status()