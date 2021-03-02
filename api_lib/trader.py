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
        self.paddle = 0
        self.init_wallet()
    
    def xauth_sign(self, json_body):
        secret_bytes = bytes(self.secret, encoding='utf-8')
        signature = hmac.new(secret_bytes, json_body.encode(), hashlib.sha256).hexdigest()
        return signature
    
    def ticker(self):
        ticker_url = ''.join(self.config['public']['public_base_url'],self.config['public']['ticker'])
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
        balance_url = ''.join(self.config['individual']['base_url'],self.config['individual']['balances'])
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
        # pprint(ticker)
        print("Estimated source funds = {}".format(self.wallet.target_balance['balance'] * ticker['last_price'] + self.wallet.source_balance['balance'] ))
        choice = input("Auto decide depending on current balances ? (yN)")
        if choice.upper() in ['Y', 'YES']:
            logging.warn("Feature not yet implemented.")
        print("First 2 paddles are for spot trading. May include a little risk but higher the investment higher the profit. 3rd paddle is to sit for riding the wave.")
        print("Suggested Application is to start from small paddles for spot trading.")
        self.paddle = float(input("Amount for spot trade (each paddle) in " + self.config['main']['source_symbol'] + ": "))
        start = 1
        if self.paddle < self.wallet.source_balance['balance']:
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
            self.wallet.paddle_1["current"][self.config['main']['target_symbol']] = self.paddle / ticker['last_price']
            self.wallet.paddle_1["current"][self.config['main']['source_symbol']] = self.paddle
            
            self.wallet.paddle_2["previous"] = {}
            self.wallet.paddle_2["current"] = {}
            self.wallet.paddle_2["current"][self.config['main']['target_symbol']] = self.paddle / ticker['last_price']
            self.wallet.paddle_2["current"][self.config['main']['source_symbol']] = self.paddle

        else:
            ticker = self.ticker()
            self.wallet.paddle_1["previous"] = {}
            self.wallet.paddle_1["current"] = {}
            self.wallet.paddle_1["current"][self.config['main']['target_symbol']] = self.paddle / ticker['last_price']
            self.wallet.paddle_1["current"][self.config['main']['source_symbol']] = self.paddle

            self.wallet.paddle_2["previous"] = {}
            self.wallet.paddle_2["current"] = {}

        logging.info("Wallet initialize completed")
        return
    
    def order_status(self, id):
        status_url = ''.join(self.config['individual']['base_url'],self.config['individual']['status'])
        timeStamp = int(round(time.time() * 1000))
        body = {
            "id": id,
            "timestamp": timeStamp
        }
        json_body = json.dumps(body, separators = (',', ':'))
        response = dcx_post(status_url, self.key, self.xauth_sign(json_body), json_body)
        return response['status']

    def buy(self):
        buy_url = ''.join(self.config['individual']['base_url'],self.config['individual']['create_order'])
        timeStamp = int(round(time.time() * 1000))
        ticker = self.ticker()
        body = {
            "side": "buy",    #Toggle between 'buy' or 'sell'.
            "order_type": "market_order", #Toggle between a 'market_order' or 'limit_order'.
            "market": ''.join(self.config['main']['target_symbol'],self.config['main']['source_symbol']), #Replace 'SNTBTC' with your desired market pair.
            "total_quantity": self.paddle / ticker['last_price'], #Replace this with the quantity you want
            "timestamp": timeStamp
        }
        json_body = json.dumps(body, separators = (',', ':'))
        response = dcx_post(buy_url, self.key, self.xauth_sign(json_body), json_body)
        order_id = response['orders'][0]['id']
        status = self.order_status(order_id)
        while status not in ['filled','rejected']:            
            time.sleep(1)
        if status == 'rejected':
            self.buy()
            return
        logging.info("BUY : {}".format(order_id))
        return order_id

    def sell(self):
        sell_url = ''.join(self.config['individual']['base_url'],self.config['individual']['create_order'])
        timeStamp = int(round(time.time() * 1000))
        ticker = self.ticker()
        body = {
            "side": "sell",    #Toggle between 'buy' or 'sell'.
            "order_type": "market_order", #Toggle between a 'market_order' or 'limit_order'.
            "market": ''.join(self.config['main']['target_symbol'],self.config['main']['source_symbol']), #Replace 'SNTBTC' with your desired market pair.
            "total_quantity": self.paddle / ticker['last_price'], #Replace this with the quantity you want
            "timestamp": timeStamp
        }
        json_body = json.dumps(body, separators = (',', ':'))
        response = dcx_post(sell_url, self.key, self.xauth_sign(json_body), json_body)
        order_id = response['orders'][0]['id']
        status = self.order_status(order_id)
        while status not in ['filled','rejected']:            
            time.sleep(1)
        if status == 'rejected':
            self.sell()
            return
        logging.info("SELL : {}".format(order_id))
        return order_id