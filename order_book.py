from collections import deque, defaultdict
from order import Order


class OrderBook:

    def __init__(self):
        self.bids = defaultdict(deque)
        self.asks = defaultdict(deque)
        self.orders = {}
        self.time = 0

    def add_order(self, order_id, side, price, quantity):

        self.time += 1
        order = Order(order_id, side, price, quantity, self.time)

        if price == 0:
            self.match_market(order)
        else:
            self.match_limit(order)

        if order.quantity > 0:
            self.add_to_book(order)
            self.orders[order_id] = order

    def cancel_order(self, order_id):

        if order_id not in self.orders:
            return

        order = self.orders.pop(order_id)

        book_side = self.bids if order.side == "BUY" else self.asks
        queue = book_side[order.price]

        for i, o in enumerate(queue):
            if o.order_id == order_id:
                del queue[i]
                break

        if not queue:
            del book_side[order.price]

    def match_limit(self, order):

        if order.side == "BUY":

            while order.quantity > 0 and self.asks:

                best_ask = min(self.asks)

                if best_ask > order.price:
                    break

                self.match(order, self.asks[best_ask])

                if not self.asks[best_ask]:
                    del self.asks[best_ask]

        else:

            while order.quantity > 0 and self.bids:

                best_bid = max(self.bids)

                if best_bid < order.price:
                    break

                self.match(order, self.bids[best_bid])

                if not self.bids[best_bid]:
                    del self.bids[best_bid]

    def match_market(self, order):

        if order.side == "BUY":

            while order.quantity > 0 and self.asks:

                best_ask = min(self.asks)

                self.match(order, self.asks[best_ask])

                if not self.asks[best_ask]:
                    del self.asks[best_ask]

        else:

            while order.quantity > 0 and self.bids:

                best_bid = max(self.bids)

                self.match(order, self.bids[best_bid])

                if not self.bids[best_bid]:
                    del self.bids[best_bid]

    def match(self, taker, maker_queue):

        while taker.quantity > 0 and maker_queue:

            maker = maker_queue[0]

            if maker.order_id == taker.order_id:
                maker_queue.popleft()
                continue

            trade_qty = min(taker.quantity, maker.quantity)

            print(f"TRADE {taker.order_id if taker.side=='BUY' else maker.order_id} "
                  f"{maker.order_id if taker.side=='BUY' else taker.order_id} "
                  f"{maker.price} {trade_qty}")

            maker.quantity -= trade_qty
            taker.quantity -= trade_qty

            if maker.quantity == 0:
                maker_queue.popleft()
                self.orders.pop(maker.order_id, None)

            else:
                break

    def add_to_book(self, order):

        side = self.bids if order.side == "BUY" else self.asks
        side[order.price].append(order)

    def print_book(self):

        print("\n--- Book ---")

        ask_levels = sorted(self.asks.keys())[:5]
        bid_levels = sorted(self.bids.keys(), reverse=True)[:5]

        for p in ask_levels:
            qty = sum(o.quantity for o in self.asks[p])
            print(f"ASK: {p} x {qty}")

        for p in bid_levels:
            qty = sum(o.quantity for o in self.bids[p])
            print(f"BID: {p} x {qty}")
