# CryptoRaid

## API KEY
Generate api key from broker account settings.

## DOC
### Terminology
#### Common
- target currency refers to the asset that is the quantity of a symbol.
- base currency refers to the asset that is the price of a symbol.
- pair uniquely idenfies the market along with it's exchange, and is available in market details api.
- ecode is used to specify the exchange for the given market. Valid values for ecode include:
  - B: Binance
  - I: CoinDCX
  - HB: HitBTC
  - H: Huobi
  - BM: BitMEX

#### Orders
- status: used to denote the current status of the given order. Valid values for status include:
  - init: order is just created, but not placed in the orderbook
  - open: order is successfully placed in the orderbook
  - partially_filled: order is partially filled
  - filled: order is completely filled
  - partially_cancelled: order is partially filled, but cancelled, thus inactive
  - cancelled: order is completely or partially cancelled
  - rejected: order is rejected (not placed on the exchange
#### Margin Orders
- status: used to denote the current status of the given margin order. Valid values for status include:
  - init: order is just created, but not placed in the orderbook
  - open: order is successfully placed in the orderbook
  - partial_entry: internal entry order is partially filled
  - partial_close: internal target order is partially closed
  - cancelled: order is completely cancelled
  - rejected: order is rejected (not placed on the exchange)
  - close: order is completely filled
  - triggered: stop varinat order triggered at specified stop price
- order_type: used to denote the type of order to be placed. Valid values for order_type includes:
  - market_order: in this order type we don't secify price; it is executed on the market price
  - limit_order: in this order type we specify the price on which order is to be executed
  - stop_limit: it is a type of limit order whether we specify stop price and a price, once price reaches stop_price, order is placed on the given price
  - take_profit: it is a type of limit order whether we specify stop price and a price, once price reaches stop_price, order is placed on the given price

> Other Terms: - target_price: The price at which the trader plans to buy/sell or close the order position is called the Target Price. When the Target price is hit, the trade is closed and the trader’s funds are settled according to the P&L incurred. Target price feature is available if the trader checks the Bracket order checkbox. - sl_price: The price at which the trader wishes to Stop Loss is the SL Price. - stop_price: It is used in the Stop Variant order, to specify stop price

#### Margin Internal Orders
- status for internal orders: used to denote the type of internal orders. Valid values for order_type includes:
  - initial: order is just created
  - open: order is successfully placed in the orderbook
  - partially_filled: order is partially filled
  - filled: order is completely filled
  - cancelled: order is completely cancelled
  - rejected: order is rejected (not placed on the exchange)
  - partially_cancelled: order is partially cancelled
  - untriggered: stop varinat order was not triggered

## TODO
- [x] create trading agent
- [x] wallet initialize
- [ ] minimum transaction amount of source
- [ ] auto calculate paddle amount[INVALID|RISKY].
- [x] paddle strategy grooming
- [ ] auto detect rising trend while buying to buy quickly
- [x] save previous wallet in a file and load if available
- [x] add beeper or text-to-speech after placing successfull orders[INVALID]
- [ ] fix start with BUY paddle print
- [ ] auto calc paddle 3 and process
- [x] libasound2-dev for beeper and tidy for console
- [ ] add proper terminator
- [x] manual entry for paddle values
- [ ] Adding BINANCE API
- [ ] Add setup for module