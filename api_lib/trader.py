from api_lib.wallet import Wallet
import configparser
import hmac, json, hashlib, time
from api_lib.dcx_requests import dcx_get, dcx_post
from api_lib.binance_requests import binance_get, binance_post
import logging
import sys
from api_lib.precision import round_down, round_up
from utils import tidy, timer


class Trader:
    def __init__(self, configpath: str) -> None:
        logging.info("Reading config from {}".format(configpath))
        self.config = configparser.ConfigParser()
        self.config.read(configpath)
        self.key = self.config["individual"]["api_key"]
        self.secret = self.config["individual"]["secret_key"]
        logging.info("Creating a Wallet for trading agent.")
        self.wallet = Wallet()
        self.paddle = 0
        self.init_wallet()

    def ticker(self) -> float:
        return 0.0

    def init_wallet(self) -> None:
        return

    def update_wallet(self) -> None:
        return

    def falling_trend(self) -> None:
        logging.info(
            "Falling trend with {}secs interval".format(self.config["main"]["trend"])
        )
        ticker_old = self.ticker()
        print("LIVE: {}".format(ticker_old["last_price"]))
        # Sleeping for 5 secs just for heads up
        logging.info("sleeping for {}".format(int(self.config["main"]["trend"])))
        timer(int(self.config["main"]["trend"]))
        while True:
            ticker_new = self.ticker()
            print("LIVE: {}".format(ticker_new["last_price"]))
            if ticker_new["last_price"] > ticker_old["last_price"]:
                return ticker_new
            logging.info("sleeping for {}".format(int(self.config["main"]["trend"])))
            timer(int(self.config["main"]["trend"]))
            tidy()
            ticker_old = ticker_new

    def rising_trend(self) -> None:
        logging.info(
            "Rising trend with {}secs interval".format(self.config["main"]["trend"])
        )
        ticker_old = self.ticker()
        print("LIVE: {}".format(ticker_old["last_price"]))
        # Sleeping for 5 secs just for heads up
        logging.info("sleeping for {}".format(int(self.config["main"]["trend"])))
        timer(int(self.config["main"]["trend"]))
        while True:
            ticker_new = self.ticker()
            print("LIVE: {}".format(ticker_new["last_price"]))
            if ticker_new["last_price"] < ticker_old["last_price"]:
                return ticker_new
            logging.info("sleeping for {}".format(int(self.config["main"]["trend"])))
            timer(int(self.config["main"]["trend"]))
            tidy()
            ticker_old = ticker_new

    def profit(self, selling: float) -> float:
        ticker = self.ticker()
        profit = (
            ticker["last_price"] * selling
            - self.paddle
            - self.paddle * float(self.config["main"]["fee"]) / 100
        )
        return profit

    def sudo_profit(self, prev_qty: float, prev_ticker: float) -> float:
        sudo_ticker = (
            prev_qty * prev_ticker
            - float(self.config["main"]["profit"])
            - self.paddle * float(self.config["main"]["fee"]) / 100
        ) / prev_qty
        return sudo_ticker

    def buy(self, qty: float, price: float) -> None:
        return

    def sell(self, qty: float, price: float) -> None:
        return


class DCX_Trader(Trader):
    def __init__(self, configpath: dict) -> None:
        super().__init__(configpath)
        self.wallet = Wallet()
        logging.info("Creating a Wallet for trading agent.")
        self.init_wallet()

    def xauth_sign(self, json_body: json) -> str:
        secret_bytes = bytes(self.secret, encoding="utf-8")
        signature = hmac.new(
            secret_bytes, json_body.encode(), hashlib.sha256
        ).hexdigest()
        return signature

    def ticker(self) -> float:
        ticker_url = (
            self.config["public"]["public_base_url"] + self.config["public"]["ticker"]
        )
        response = dcx_get(ticker_url)
        ticker_id = -1
        for i in range(len(response)):
            if (
                response[i]["market"]
                == self.config["main"]["target_symbol"]
                + self.config["main"]["source_symbol"]
            ):
                ticker_id = i
                break
        if ticker_id < 0:
            logging.error(
                "Invalid Target symbol and Source symbol. Check configurations."
            )
            sys.exit()
        for key in response[ticker_id]:
            try:
                response[ticker_id][key] = float(response[ticker_id][key])
            except:
                logging.debug("Non float value.")
        logging.debug("Ticker : {}".format(response[ticker_id]["last_price"]))
        return response[ticker_id]

    def get_order(self, id: int) -> dict:
        status_url = (
            self.config["individual"]["base_url"] + self.config["individual"]["status"]
        )
        timeStamp = int(round(time.time() * 1000))
        body = {"id": id, "timestamp": timeStamp}
        json_body = json.dumps(body, separators=(",", ":"))
        response = dcx_post(status_url, self.key, self.xauth_sign(json_body), json_body)
        logging.info("DCX : {}".format(json.dumps(response)))
        return response

    def buy(self) -> None:
        buy_url = (
            self.config["individual"]["base_url"]
            + self.config["individual"]["create_order"]
        )
        timeStamp = int(round(time.time() * 1000))
        ticker = self.ticker()
        body = {
            "side": "buy",  # Toggle between 'buy' or 'sell'.
            "order_type": "market_order",  # Toggle between a 'market_order' or 'limit_order'.
            "market": self.config["main"]["target_symbol"]
            + self.config["main"][
                "source_symbol"
            ],  # Replace 'SNTBTC' with your desired market pair.
            "total_quantity": round_up(
                self.paddle / ticker["last_price"], 5
            ),  # Replace this with the quantity you want
            "timestamp": timeStamp,
        }
        json_body = json.dumps(body, separators=(",", ":"))
        response = dcx_post(buy_url, self.key, self.xauth_sign(json_body), json_body)
        logging.info("DCX : {}".format(json.dumps(response)))
        order_id = response["orders"][0]["id"]
        status = self.get_order(order_id)["status"]
        while status not in ["filled", "rejected"]:
            timer(1)
            status = self.get_order(order_id)["status"]
        if status == "rejected":
            self.buy()
            return
        logging.info("BUY : {}".format(order_id))
        return self.get_order(order_id)

    def sell(self, quantity: float) -> dict:
        sell_url = (
            self.config["individual"]["base_url"]
            + self.config["individual"]["create_order"]
        )
        timeStamp = int(round(time.time() * 1000))
        ticker = self.ticker()
        body = {
            "side": "sell",  # Toggle between 'buy' or 'sell'.
            "order_type": "market_order",  # Toggle between a 'market_order' or 'limit_order'.
            "market": self.config["main"]["target_symbol"]
            + self.config["main"][
                "source_symbol"
            ],  # Replace 'SNTBTC' with your desired market pair.
            "total_quantity": round_down(
                quantity, 5
            ),  # Replace this with the quantity you want
            "timestamp": timeStamp,
        }
        json_body = json.dumps(body, separators=(",", ":"))
        response = dcx_post(sell_url, self.key, self.xauth_sign(json_body), json_body)
        logging.info("DCX : {}".format(json.dumps(response)))
        order_id = response["orders"][0]["id"]
        status = self.get_order(order_id)["status"]
        while status not in ["filled", "rejected"]:
            timer(1)
            status = self.get_order(order_id)["status"]
        if status == "rejected":
            self.sell()
            return
        logging.info("SELL : {}".format(order_id))
        return self.get_order(order_id)

    def init_wallet(self) -> None:
        balance_url = (
            self.config["individual"]["base_url"]
            + self.config["individual"]["balances"]
        )
        timeStamp = int(round(time.time() * 1000))
        body = {"timestamp": timeStamp}
        json_body = json.dumps(body, separators=(",", ":"))
        response = dcx_post(
            balance_url, self.key, self.xauth_sign(json_body), json_body
        )
        for i in response:
            if i["currency"] == self.config["main"]["target_symbol"]:
                self.wallet.target_balance = i
                self.wallet.target_balance["balance"] = float(
                    self.wallet.target_balance["balance"]
                )
            if i["currency"] == self.config["main"]["source_symbol"]:
                self.wallet.source_balance = i
                self.wallet.source_balance["balance"] = float(
                    self.wallet.source_balance["balance"]
                )

        logging.info("Source balance: {}".format(self.wallet.source_balance))
        logging.info("Target balance: {}".format(self.wallet.target_balance))
        logging.info("Starting 3-way paddle strategy")
        logging.info(
            "Decide the paddle source_amount. (Suggested to refer previous transactions)"
        )
        ticker = self.ticker()
        logging.info(
            "Estimated source funds = {}".format(
                self.wallet.target_balance["balance"] * ticker["last_price"]
                + self.wallet.source_balance["balance"]
            )
        )
        # choice = input("Auto decide depending on current balances ? (yN)")
        # if choice.upper() in ['Y', 'YES']:
        #     logging.warn("Feature not yet implemented.")
        logging.info(
            "First 2 paddles are for spot trading. May include a little risk but higher the investment higher the profit. 3rd paddle is to sit for riding the wave."
        )
        logging.info(
            "Suggested Application is to start from small paddles for spot trading."
        )
        try:
            self.paddle = float(
                input(
                    "Amount for spot trade (each paddle) in "
                    + self.config["main"]["source_symbol"]
                    + ": "
                )
            )
        except Exception as e:
            logging.error(e)
            logging.info("Wallet initialization restarted.")
            self.init_wallet()
            pass
        start = 1
        if self.paddle < self.wallet.source_balance["balance"]:
            choice = input("Start by ? (BUY/sell)")
            if choice.upper() in ["SELL", "S"]:
                start = -1
        else:
            start = -1
        # 1 means start by buying ; -1 means start by sell
        if start == -1:
            choice = input("Auto Choose paddle Values? [yN] ")
            if choice.upper() in ["Y", "YES"]:
                ticker = self.falling_trend()
                self.wallet.paddle_1["previous"] = {}
                self.wallet.paddle_1["current"] = {}
                self.wallet.paddle_1["current"][
                    self.config["main"]["target_symbol"]
                ] = (self.paddle / ticker["last_price"])
                self.wallet.paddle_1["current"][
                    self.config["main"]["source_symbol"]
                ] = ticker["last_price"]

                self.wallet.paddle_2["previous"] = {}
                self.wallet.paddle_2["current"] = {}
                self.wallet.paddle_2["current"][
                    self.config["main"]["target_symbol"]
                ] = (self.paddle / ticker["last_price"])
                self.wallet.paddle_2["current"][
                    self.config["main"]["source_symbol"]
                ] = ticker["last_price"]
            else:
                paddle_1_source = float(
                    input("Enter ticker previously bought at for paddle 1 : ")
                )
                paddle_2_source = float(
                    input("Enter ticker previously bought at for paddle 2 : ")
                )
                self.wallet.paddle_1["current"] = {}
                self.wallet.paddle_1["previous"] = {}
                self.wallet.paddle_1["current"][
                    self.config["main"]["target_symbol"]
                ] = (self.paddle / paddle_1_source)
                self.wallet.paddle_1["current"][
                    self.config["main"]["source_symbol"]
                ] = paddle_1_source
                self.wallet.paddle_2["current"] = {}
                self.wallet.paddle_2["previous"] = {}
                self.wallet.paddle_2["current"][
                    self.config["main"]["target_symbol"]
                ] = (self.paddle / paddle_2_source)
                self.wallet.paddle_2["current"][
                    self.config["main"]["source_symbol"]
                ] = paddle_2_source

        else:
            choice = input("Auto Choose paddle Values? [yN] ")
            if choice.upper() in ["Y", "YES"]:
                ticker = self.falling_trend()
                self.wallet.paddle_1["previous"] = {}
                self.wallet.paddle_1["current"] = {}
                self.wallet.paddle_1["current"][
                    self.config["main"]["target_symbol"]
                ] = (self.paddle / ticker["last_price"])
                self.wallet.paddle_1["current"][
                    self.config["main"]["source_symbol"]
                ] = ticker["last_price"]
            else:
                paddle_1_source = float(
                    input("Enter ticker previously bought at for paddle 1 : ")
                )
                self.wallet.paddle_1["current"] = {}
                self.wallet.paddle_1["previous"] = {}
                self.wallet.paddle_1["current"][
                    self.config["main"]["target_symbol"]
                ] = (self.paddle / paddle_1_source)
                self.wallet.paddle_1["current"][
                    self.config["main"]["source_symbol"]
                ] = paddle_1_source

            self.wallet.paddle_2["previous"] = {}
            self.wallet.paddle_2["current"] = {}

        print("Paddle 1:")
        print(json.dumps(self.wallet.paddle_1, indent=4))
        print("Paddle 2:")
        print(json.dumps(self.wallet.paddle_2, indent=4))

        logging.info("Wallet initialize completed")
        return

    def update_wallet(self) -> None:
        balance_url = (
            self.config["individual"]["base_url"]
            + self.config["individual"]["balances"]
        )
        timeStamp = int(round(time.time() * 1000))
        body = {"timestamp": timeStamp}
        json_body = json.dumps(body, separators=(",", ":"))
        response = dcx_post(
            balance_url, self.key, self.xauth_sign(json_body), json_body
        )
        for i in response:
            if i["currency"] == self.config["main"]["target_symbol"]:
                self.wallet.target_balance = i
                self.wallet.target_balance["balance"] = float(
                    self.wallet.target_balance["balance"]
                )
            if i["currency"] == self.config["main"]["source_symbol"]:
                self.wallet.source_balance = i
                self.wallet.source_balance["balance"] = float(
                    self.wallet.source_balance["balance"]
                )


class Binance_Trader(Trader):
    def __init__(self, configpath: dict) -> None:
        super().__init__(configpath)
        self.config
        self.key = self.config["binance"]["api_key"]
        self.secret = self.config["binance"]["api_secret"]
        self.symbol = (
            self.config["main"]["target_symbol"] + self.config["main"]["source_symbol"]
        )
        logging.info("Creating a Wallet for trading agent.")
        self.init_wallet()

    def ticker(self) -> float:
        url = self.conf["binance"]["base_url"] + self.conf["binance"]["ticker"]
        key = self.conf["binance"]["api_key"]
        params = {"symbol": self.symbol}
        return float(binance_get(url, key, params=params).get("price"))

    def init_wallet(self) -> None:
        balance_url = (
            self.config["binance"]["base_url"] + self.config["binance"]["balances"]
        )
        timeStamp = int(round(time.time() * 1000))
        body = {"timestamp": timeStamp}
        

    def update_wallet(self) -> None:
        return

    def buy(self, amount: float) -> None:
        pass

    def sell(self, amount: float) -> None:
        pass

    def get_order(self, order_id: str) -> None:
        pass
