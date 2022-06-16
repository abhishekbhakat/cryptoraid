import json
import logging
from utils import tidy2, timer, tidy
from pprint import pprint
from api_lib.trader import DCX_Trader

def stack_primary(trader:DCX_Trader)->None:
    trader.update_wallet()
    with open(trader.config['logging']['wallet_log'],'wt') as f:
        json.dump(trader.wallet.get(), f, indent=4)
    ticker = trader.ticker()
    print("LIVE : {}".format(str(ticker['last_price'])))
    if trader.wallet.paddle_1['current'] == {} and trader.wallet.paddle_2['current'] != {}:
        pass
    elif trader.wallet.paddle_2['current'] == {} and trader.wallet.paddle_1['current'] != {}:
        pass
    elif trader.wallet.paddle_1['current'] == {} and trader.wallet.paddle_2['current'] == {}:
        pass
    else:
        pass

    logging.info("sleeping for {}".format(int(trader.config['main']['interval'])))   
    timer(int(trader.config['main']['interval']))
    tidy2()