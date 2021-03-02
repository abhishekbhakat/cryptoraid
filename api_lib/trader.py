from requests.models import Response
from api_lib.wallet import Wallet
import configparser
import hmac, json, hashlib, time
from api_lib.dcx_requests import dcx_get, dcx_post
from pprint import pprint 
import logging
import sys

class Trader():

    def __init__(self, configpath):
        logging.info("Reading config from {}".format(configpath))
        self.config = configparser.ConfigParser()
        self.config.read(configpath)
        self.key = self.config['individual']['api_key']
        self.secret = self.config['individual']['secret_key']
        logging.info("Creating a Wallet for trading agent.")
        self.ticker_id = -1
        self.wallet = Wallet()
        self.init_wallet()
    
    def xauth_sign(self, json_body):
        secret_bytes = bytes(self.secret, encoding='utf-8')
        signature = hmac.new(secret_bytes, json_body.encode(), hashlib.sha256).hexdigest()
        return signature
    
    def ticker(self):
        ticker_url = self.config['public']['public_base_url'] + self.config['public']['ticker']
        response = dcx_get(ticker_url)
        if self.ticker_id < 0:
            for i in range(len(response)):
                if response[i]['market'] == self.config['main']['target_symbol'] + self.config['main']['source_symbol']:
                    self.ticker_id = i
                    
                    break
        if self.ticker_id < 0:
            logging.error("Invalid Target symbol and Source symbol. Check configurations.")
            sys.exit()
        for key in response[self.ticker_id]:
            try:
                response[self.ticker_id][key] = float(response[self.ticker_id][key])
            except:
                logging.debug("Non float value.")
        return response[self.ticker_id]

    def init_wallet(self):
        # Total money source
        # Total money target
        balance_url = self.config['individual']['base_url'] + self.config['individual']['balances']
        timeStamp = int(round(time.time() * 1000))
        body = {"timestamp" : timeStamp}
        json_body = json.dumps(body, separators = (',', ':'))
        response = dcx_post(balance_url, self.key, self.xauth_sign(json_body), json_body)
        for i in response:
            if i['currency'] == self.config['main']['target_symbol'] :
                self.wallet.target_balance = i
                self.wallet.target_balance['balance'] = float(self.wallet.target_balance['balance'])
            if i['currency'] == self.config['main']['source_symbol'] :
                self.wallet.source_balance = i
                self.wallet.source_balance['balance'] = float(self.wallet.source_balance['balance'])
        
        logging.info("Source balance: {}".format(self.wallet.source_balance))
        logging.info("Target balance: {}".format(self.wallet.target_balance))
        print("Starting 3-way paddle strategy")
        print("Decide the paddle source_amount. (Suggested to refer previous transactions)")
        ticker = self.ticker()
        pprint(ticker)
        print("Estimated source funds = {}".format(self.wallet.target_balance['balance'] * ticker['last_price'] + self.wallet.source_balance['balance'] ))
        choice = input("Auto decide depending on current balances ? (yN)")
        if choice.upper() in ['Y', 'YES']:
            logging.warn("Feature not yet implemented.")
        print("First 2 paddles are for spot trading. May include a little risk but higher the investment higher the profit. 3rd paddle is to sit for riding the wave.")
        print("Suggested Application is to start from small paddles for spot trading.")
        paddle = float(input("Amount for spot trade (each paddle) in " + self.config['main']['source_symbol'] + ": "))
        start = 1
        if paddle < self.wallet.source_balance['balance']:
            choice = input("Start by ? (BUY/sell)")
            if choice.upper() in ['SELL', 'S']:
                start = -1
        else:
            start = -1
        # 1 means start by buying ; -1 means start by sell
        if start == -1:
            ticker = self.ticker()
            self.wallet.paddle_1["previous"] = {}
            self.wallet.paddle_1["current"] = {}
            self.wallet.paddle_1["current"][self.config['main']['target_symbol']] = paddle / ticker['last_price']
            self.wallet.paddle_1["current"][self.config['main']['source_symbol']] = paddle
            
            self.wallet.paddle_2["previous"] = {}
            self.wallet.paddle_2["current"] = {}
            self.wallet.paddle_2["current"][self.config['main']['target_symbol']] = paddle / ticker['last_price']
            self.wallet.paddle_2["current"][self.config['main']['source_symbol']] = paddle

        else:
            ticker = self.ticker()
            self.wallet.paddle_1["previous"] = {}
            self.wallet.paddle_1["current"] = {}
            self.wallet.paddle_1["current"][self.config['main']['target_symbol']] = paddle / ticker['last_price']
            self.wallet.paddle_1["current"][self.config['main']['source_symbol']] = paddle

            self.wallet.paddle_2["previous"] = {}
            self.wallet.paddle_2["current"] = {}

        

        logging.info("Wallet initialize completed")
        return
        

