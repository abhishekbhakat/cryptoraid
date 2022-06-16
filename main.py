
from api_lib.trader import DCX_Trader
import time
from art import *
import logging

import json
from configparser import ConfigParser
from trade_process.stack_secondary import stack_secondary
from trade_process.stack_primary import stack_primary

conf = ConfigParser()
conf.read('config.ini')
logging.basicConfig(level=conf['core']['logging'])
welcome = text2art("Cryptoraid v"+conf['core']['version'])

logging.info("\n{}".format(welcome))
logging.info("Creating a trading agent.")
trader = DCX_Trader("config.ini")

# singleton infinite loop
logging.info("Watcher init")
while True:
    # Solution Strategy
    # Place order which seems to be executing successfully, don't try to be whale.
    stack_primary(trader)