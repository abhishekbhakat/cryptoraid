from pprint import pprint
from api_lib.trader import Trader
import time
from art import *
import logging

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
        logging.info("Buying Paddle 1")
        pprint(trader.wallet.paddle_1)
        if trader.wallet.paddle_1['previous'] != {}:
            while ticker['last_price'] > trader.sudo_profit(trader.wallet.paddle_1['previous'][trader.config['main']['target_symbol']], trader.wallet.paddle_1['previous'][trader.config['main']['source_symbol']]) :
                print("Expected buy at {}".format(trader.sudo_profit(trader.wallet.paddle_1['previous'][trader.config['main']['target_symbol']], trader.wallet.paddle_1['previous'][trader.config['main']['source_symbol']])))
                logging.info("sleeping for {}".format(int(trader.config['main']['interval'])))
                time.sleep(int(trader.config['main']['interval']))
                ticker = trader.ticker()
            else:
                ticker = trader.falling_trend()
                order = trader.buy()
                trader.wallet.paddle_1['current'][trader.config['main']['target_symbol']] = order['total_quantity']
                trader.wallet.paddle_1['current'][trader.config['main']['source_symbol']] = order['avg_price']
        else:
            ticker = trader.falling_trend()
            order = trader.buy()
            trader.wallet.paddle_1['current'][trader.config['main']['target_symbol']] = order['total_quantity']
            trader.wallet.paddle_1['current'][trader.config['main']['source_symbol']] = order['avg_price']

        logging.info("Selling paddle 2")
        pprint(trader.wallet.paddle_2)
        ticker = trader.ticker()
        while trader.profit(trader.wallet.paddle_2['current'][trader.config['main']['target_symbol']]) < float(trader.config['main']['profit']) :
            print("Appx. profit = {}".format(trader.profit(trader.wallet.paddle_2['current'][trader.config['main']['target_symbol']])))
            logging.info("sleeping for {}".format(int(trader.config['main']['interval'])))
            time.sleep(int(trader.config['main']['interval']))
            ticker = trader.ticker()
        else:
            ticker = trader.rising_trend()
            print("Appx. profit = {}".format(trader.profit(trader.wallet.paddle_2['current'][trader.config['main']['target_symbol']])))
            order = trader.sell(trader.paddle/ticker['last_price'])
            trader.wallet.paddle_2['previous'][trader.config['main']['target_symbol']] = order['total_quantity']
            trader.wallet.paddle_2['previous'][trader.config['main']['source_symbol']] = order['avg_price']
            trader.wallet.paddle_2['current'] = {}

    elif trader.wallet.paddle_2['current'] == {} and trader.wallet.paddle_1['current'] != {}:
        logging.info("Buying Paddle 2")
        pprint(trader.wallet.paddle_2)
        if trader.wallet.paddle_1['previous'] != {}:
            while ticker['last_price'] > trader.sudo_profit(trader.wallet.paddle_2['previous'][trader.config['main']['target_symbol']], trader.wallet.paddle_2['previous']['source_symbol']) :
                print("Expected buy at {}".format(trader.sudo_profit(trader.wallet.paddle_2['previous'][trader.config['main']['target_symbol']], trader.wallet.paddle_2['previous']['source_symbol'])))
                logging.info("sleeping for {}".format(int(trader.config['main']['interval'])))
                time.sleep(int(trader.config['main']['interval']))
                ticker = trader.ticker()
            else:
                ticker = trader.falling_trend()
                order = trader.buy()
                trader.wallet.paddle_2['current'][trader.config['main']['target_symbol']] = order['total_quantity']
                trader.wallet.paddle_2['current'][trader.config['main']['source_symbol']] = order['avg_price']
        else:
            ticker = trader.falling_trend()
            order = trader.buy()
            trader.wallet.paddle_2['current'][trader.config['main']['target_symbol']] = order['total_quantity']
            trader.wallet.paddle_2['current'][trader.config['main']['source_symbol']] = order['avg_price']

        logging.info("Selling Paddle 1")
        pprint(trader.wallet.paddle_1)
        ticker = trader.ticker()
        while trader.profit(trader.wallet.paddle_1['current'][trader.config['main']['target_symbol']]) < float(trader.config['main']['profit']) :
            print("Appx. profit = {}".format(trader.profit(trader.wallet.paddle_1['current'][trader.config['main']['target_symbol']])))
            logging.info("sleeping for {}".format(int(trader.config['main']['interval'])))
            time.sleep(int(trader.config['main']['interval']))
            ticker = trader.ticker()
        else:
            ticker = trader.rising_trend()
            print("Appx. profit = {}".format(trader.profit(trader.wallet.paddle_1['current'][trader.config['main']['target_symbol']])))
            order = trader.sell(trader.paddle/ticker['last_price'])
            trader.wallet.paddle_1['previous'][trader.config['main']['target_symbol']] = order['total_quantity']
            trader.wallet.paddle_1['previous'][trader.config['main']['source_symbol']] = order['avg_price']
            trader.wallet.paddle_1['current'] = {}

    elif trader.wallet.paddle_1['current'] == {} and trader.wallet.paddle_2['current'] == {}:
        logging.info("Buying Paddle 1")
        pprint(trader.wallet.paddle_1)
        ticker = trader.falling_trend()
        order = trader.buy()
        trader.wallet.paddle_1['current'][trader.config['main']['target_symbol']] = order['total_quantity']
        trader.wallet.paddle_1['current'][trader.config['main']['source_symbol']] = order['avg_price']

    else:
        print("Appx. profit = {}".format(trader.profit(trader.wallet.paddle_1['current'][trader.config['main']['target_symbol']])))
        if trader.profit(trader.wallet.paddle_1['current'][trader.config['main']['target_symbol']]) > float(trader.config['main']['profit']) :
            ticker = trader.rising_trend()
            print("Appx. profit = {}".format(trader.profit(trader.wallet.paddle_1['current'][trader.config['main']['target_symbol']])))
            logging.info("Selling Paddle 1")
            pprint(trader.wallet.paddle_1)
            order = trader.sell(trader.wallet.paddle_1['current'][trader.config['main']['target_symbol']])
            trader.wallet.paddle_1['previous'][trader.config['main']['target_symbol']] = order['total_quantity']
            trader.wallet.paddle_1['previous'][trader.config['main']['source_symbol']] = order['avg_price']
            trader.wallet.paddle_1['current'] = {}

        elif trader.profit(trader.wallet.paddle_2['current'][trader.config['main']['target_symbol']]) > float(trader.config['main']['profit']):
            ticker = trader.rising_trend()
            print("Appx. profit = {}".format(trader.profit(trader.wallet.paddle_2['current'][trader.config['main']['target_symbol']])))
            logging.info("Selling Paddle 1")
            pprint(trader.wallet.paddle_1)
            order = trader.sell(trader.wallet.paddle_2['current'][trader.config['main']['target_symbol']])
            trader.wallet.paddle_2['previous'][trader.config['main']['target_symbol']] = order['total_quantity']
            trader.wallet.paddle_2['previous'][trader.config['main']['source_symbol']] = order['avg_price']
            trader.wallet.paddle_2['current'] = {}
    logging.info("sleeping for {}".format(int(trader.config['main']['interval'])))   
    time.sleep(int(trader.config['main']['interval']))