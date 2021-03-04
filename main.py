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
    # Conditions for what step to take
    # Remember to update wallet after successfull execution of order
    # Place order which seems to be executing successfully, don't try to be whale.
    ticker = trader.ticker()
    print("LIVE : {}".format(ticker['last_price']))
    if trader.wallet.paddle_1['current'] == {} and trader.wallet.paddle_2['current'] != {}:
        # Buy paddle_1

        # Sell paddle_2
        pass
    elif trader.wallet.paddle_2['current'] == {} and trader.wallet.paddle_1['current'] != {}:
        # Buy paddle_2
        # Sell paddle_1
        pass
    elif trader.wallet.paddle_1['current'] == {} and trader.wallet.paddle_2['current'] == {}:
        # Buy paddle_1
        pass
    else:
        if (ticker['last_price'] * trader.wallet.paddle_1['current'][trader.config['main']['target_symbol']]) > ( trader.paddle + float(trader.config['main']['profit']) + trader.paddle * float(trader.config['main']['fee']) / 100 ) :
            print("CAN SELL PADDLE 1")

        elif (ticker['last_price'] * trader.wallet.paddle_2['current'][trader.config['main']['target_symbol']]) > ( trader.paddle + float(trader.config['main']['profit']) + trader.paddle * float(trader.config['main']['fee']) / 100 ) :
            print("CAN SELL PADDLE 2")

        pass
    time.sleep(int(trader.config['main']['interval']))