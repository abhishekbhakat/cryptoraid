from api_lib.wallet import Wallet
from api_lib.trader import Trader
from api_lib.wallet import Wallet
from api_lib.dcx_requests import dcx_get, dcx_post
import time
from pprint import pprint 



# init trader
trader_1 = Trader("config.ini")
trader_1.wallet = Wallet()

# singleton infinite loop
while True:
    # solution strategy
    pprint(dcx_get(trader_1.config['public']['public_base_url']))

    time.sleep(5)