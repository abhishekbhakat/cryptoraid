import configparser
import hmac, json, hashlib, time

class Trader():

    def __init__(self, configpath):
        self.config = configparser.ConfigParser()
        self.config.read(configpath)
        self.key = self.config['individual']['api_key']
        self.wallet = None
    
    def xauth_sign(self, body = {}):
        timeStamp = int(round(time.time() * 1000))
        body["timestamp"]= timeStamp
        json_body = json.dumps(body, separators = (',', ':'))
        secret_bytes = bytes(self.config['individual']['secret_key'], encoding='utf-8')
        signature = hmac.new(secret_bytes, json_body.encode(), hashlib.sha256).hexdigest()
        return signature