from api_lib.trader import Trader
import time
from art import *
import logging

logging.basicConfig(level=logging.INFO)
welcome = text2art("Cryptoraid v0.1.0")

logging.info("\n{}".format(welcome))
logging.info("Creating a trading agent.")
trader_1 = Trader("config.ini")

# singleton infinite loop
logging.info("Watcher init")
while True:
    # solution strategy
    time.sleep(int(trader_1.config['main']['interval']))