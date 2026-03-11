# In-Memory Order Book Engine

This project implements a simple in-memory limit order book for a single instrument.

## Features

- Limit orders
- Market orders
- Price-time priority matching
- Order cancellation
- Partial fills
- Final order book snapshot

## Design

Two order sides are maintained:

Bids
- Buy orders
- Sorted highest price first

Asks
- Sell orders
- Sorted lowest price first

Each price level stores orders in FIFO order using deque to maintain time priority.

## Data Structures

bids: dict(price -> deque of orders)

asks: dict(price -> deque of orders)

orders: dict(order_id -> order)

## Matching Logic

Buy orders match lowest ask.

Sell orders match highest bid.

Trades execute at the resting order price.

## Run

python main.py < input.txt


## Example

### Input


O1 BUY 100.50 10
O2 BUY 100.50 5
O3 SELL 100.50 8
O4 SELL 99.00 20
CANCEL O2


### Output


TRADE O1 O3 100.50 8
TRADE O1 O4 99.00 2

--- Book ---
ASK: 99.00 x 18