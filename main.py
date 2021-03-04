from api_lib.trader import Trader
import time
from art import *
import logging
from datetime import timedelta

logging.basicConfig(level=logging.INFO)
welcome = text2art("Cryptoraid v0.1.0")

logging.info("\n{}".format(welcome))
logging.info("Creating a trading agent.")
trader = Trader("config.ini")

# singleton infinite loop
logging.info("Watcher init")
while True:
    # Solution Strategy
    # Place order which seems to be executing successfully, don't try to be whale.
    ticker = trader.ticker()
    print("LIVE : {}".format(ticker['last_price']))
    if trader.wallet.paddle_1['current'] == {} and trader.wallet.paddle_2['current'] != {}:
        # Buy paddle_1
        while ticker['last_price'] > trader.sudo_profit(trader.wallet.paddle_1['previous']['target_symbol'], trader.wallet.paddle_1['previous']['source_symbol']) :
            time.sleep(int(trader.config['main']['interval']))
            ticker = trader.ticker()
        else:
            ticker = trader.falling_trend()
            order = trader.buy()
            trader.wallet.paddle_1['current'][trader.config['main']['target_symbol']] = order['total_quantity']
            trader.wallet.paddle_1['current'][trader.config['main']['source_symbol']] = order['avg_price']
        # Sell paddle_2
        ticker = trader.ticker()
        while trader.profit(trader.wallet.paddle_2['current'][trader.config['main']['target_symbol']]) < float(trader.config['main']['profit']) :
            time.sleep(int(trader.config['main']['interval']))
            ticker = trader.ticker()
        else:
            ticker = trader.rising_trend()
            order = trader.sell(trader.paddle/ticker['last_price'])
            trader.wallet.paddle_2['previous'][trader.config['main']['target_symbol']] = order['total_quantity']
            trader.wallet.paddle_2['previous'][trader.config['main']['source_symbol']] = order['avg_price']
            trader.wallet.paddle_2['current'] = {}

    elif trader.wallet.paddle_2['current'] == {} and trader.wallet.paddle_1['current'] != {}:
        # Buy paddle_2
        while ticker['last_price'] > trader.sudo_profit(trader.wallet.paddle_2['previous']['target_symbol'], trader.wallet.paddle_2['previous']['source_symbol']) :
            time.sleep(int(trader.config['main']['interval']))
            ticker = trader.ticker()
        else:
            ticker = trader.falling_trend()
            order = trader.buy()
            trader.wallet.paddle_2['current'][trader.config['main']['target_symbol']] = order['total_quantity']
            trader.wallet.paddle_2['current'][trader.config['main']['source_symbol']] = order['avg_price']
        # Sell paddle_1
        ticker = trader.ticker()
        while trader.profit(trader.wallet.paddle_1['current'][trader.config['main']['target_symbol']]) < float(trader.config['main']['profit']) :
            time.sleep(int(trader.config['main']['interval']))
            ticker = trader.ticker()
        else:
            ticker = trader.rising_trend()
            order = trader.sell(trader.paddle/ticker['last_price'])
            trader.wallet.paddle_1['previous'][trader.config['main']['target_symbol']] = order['total_quantity']
            trader.wallet.paddle_1['previous'][trader.config['main']['source_symbol']] = order['avg_price']
            trader.wallet.paddle_1['current'] = {}

    elif trader.wallet.paddle_1['current'] == {} and trader.wallet.paddle_2['current'] == {}:
        # Buy paddle_1
        ticker = trader.falling_trend()
        order = trader.buy()
        trader.wallet.paddle_1['current'][trader.config['main']['target_symbol']] = order['total_quantity']
        trader.wallet.paddle_1['current'][trader.config['main']['source_symbol']] = order['avg_price']

    else:
        print("Appx. profit = {}".format(trader.profit(trader.wallet.paddle_1['current'][trader.config['main']['target_symbol']])))
        if trader.profit(trader.wallet.paddle_1['current'][trader.config['main']['target_symbol']]) > float(trader.config['main']['profit']) :
            ticker = trader.rising_trend()
            print("CAN SELL PADDLE 1")
            order = trader.sell(trader.wallet.paddle_1['current'][trader.config['main']['target_symbol']])
            trader.wallet.paddle_1['previous'][trader.config['main']['target_symbol']] = order['total_quantity']
            trader.wallet.paddle_1['previous'][trader.config['main']['source_symbol']] = order['avg_price']
            trader.wallet.paddle_1['current'] = {}

        elif trader.profit(trader.wallet.paddle_2['current'][trader.config['main']['target_symbol']]) > float(trader.config['main']['profit']):
            ticker = trader.rising_trend()
            print("CAN SELL PADDLE 2")
            order = trader.sell(trader.wallet.paddle_2['current'][trader.config['main']['target_symbol']])
            trader.wallet.paddle_2['previous'][trader.config['main']['target_symbol']] = order['total_quantity']
            trader.wallet.paddle_2['previous'][trader.config['main']['source_symbol']] = order['avg_price']
            trader.wallet.paddle_2['current'] = {}
        
    time.sleep(int(trader.config['main']['interval']))