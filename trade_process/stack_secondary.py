import json
import logging
from utils import tidy2, timer, tidy
from pprint import pprint
from api_lib.trader import Trader

def stack_secondary(trader:Trader)->None:
    trader.update_wallet()
    with open(trader.config['logging']['wallet_log'],'wt') as f:
    #     f.write(trader.wallet.__str__())
        json.dump(trader.wallet.get(), f, indent=4)
    ticker = trader.ticker()
    print("LIVE : {}".format(ticker['last_price']))
    if trader.wallet.paddle_1['current'] == {} and trader.wallet.paddle_2['current'] != {}:
        logging.info("Buying Paddle 1 as its is empty")
        pprint(trader.wallet.paddle_1)
        if trader.wallet.paddle_1['previous'] != {}:
            while ticker['last_price'] > trader.sudo_profit(trader.wallet.paddle_1['previous'][trader.config['main']['target_symbol']], trader.wallet.paddle_1['previous'][trader.config['main']['source_symbol']]) :
                print("Expected buy at {}".format(trader.sudo_profit(trader.wallet.paddle_1['previous'][trader.config['main']['target_symbol']], trader.wallet.paddle_1['previous'][trader.config['main']['source_symbol']])))
                logging.info("sleeping for {}".format(int(trader.config['main']['interval'])))
                timer(int(trader.config['main']['interval']))
                tidy()
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

        logging.info("Selling paddle 2 after buying paddle 1")
        pprint(trader.wallet.paddle_2)
        ticker = trader.ticker()
        while trader.profit(trader.wallet.paddle_2['current'][trader.config['main']['target_symbol']]) < float(trader.config['main']['profit']) :
            print("Appx. profit = {}".format(trader.profit(trader.wallet.paddle_2['current'][trader.config['main']['target_symbol']])))
            logging.info("sleeping for {}".format(int(trader.config['main']['interval'])))
            timer(int(trader.config['main']['interval']))
            tidy()
            ticker = trader.ticker()
        else:
            ticker = trader.rising_trend()
            print("Appx. profit = {}".format(trader.profit(trader.wallet.paddle_2['current'][trader.config['main']['target_symbol']])))
            order = trader.sell(trader.paddle/ticker['last_price'])
            trader.wallet.paddle_2['previous'][trader.config['main']['target_symbol']] = order['total_quantity']
            trader.wallet.paddle_2['previous'][trader.config['main']['source_symbol']] = order['avg_price']
            trader.wallet.paddle_2['current'] = {}

    elif trader.wallet.paddle_2['current'] == {} and trader.wallet.paddle_1['current'] != {}:
        logging.info("Buying paddle 2 as its empty")
        pprint(trader.wallet.paddle_2)
        if trader.wallet.paddle_1['previous'] != {}:
            while ticker['last_price'] > trader.sudo_profit(trader.wallet.paddle_2['previous'][trader.config['main']['target_symbol']], trader.wallet.paddle_2['previous'][trader.config['main']['source_symbol']]) :
                print("Expected buy at {}".format(trader.sudo_profit(trader.wallet.paddle_2['previous'][trader.config['main']['target_symbol']], trader.wallet.paddle_2['previous'][trader.config['main']['source_symbol']])))
                logging.info("sleeping for {}".format(int(trader.config['main']['interval'])))
                timer(int(trader.config['main']['interval']))
                tidy()
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

        logging.info("Selling Paddle 1 after buying paddle 2")
        pprint(trader.wallet.paddle_1)
        ticker = trader.ticker()
        while trader.profit(trader.wallet.paddle_1['current'][trader.config['main']['target_symbol']]) < float(trader.config['main']['profit']) :
            print("Appx. profit = {}".format(trader.profit(trader.wallet.paddle_1['current'][trader.config['main']['target_symbol']])))
            logging.info("sleeping for {}".format(int(trader.config['main']['interval'])))
            timer(int(trader.config['main']['interval']))
            tidy()
            ticker = trader.ticker()
        else:
            ticker = trader.rising_trend()
            print("Appx. profit = {}".format(trader.profit(trader.wallet.paddle_1['current'][trader.config['main']['target_symbol']])))
            order = trader.sell(trader.paddle/ticker['last_price'])
            trader.wallet.paddle_1['previous'][trader.config['main']['target_symbol']] = order['total_quantity']
            trader.wallet.paddle_1['previous'][trader.config['main']['source_symbol']] = order['avg_price']
            trader.wallet.paddle_1['current'] = {}

    elif trader.wallet.paddle_1['current'] == {} and trader.wallet.paddle_2['current'] == {}:
        logging.info("Buying paddle 1 as both are empty")
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
    timer(int(trader.config['main']['interval']))
    tidy2()