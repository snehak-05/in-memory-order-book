import sys
from order_book import OrderBook

book = OrderBook()

for line in sys.stdin:

    parts = line.strip().split()

    if not parts:
        continue

    if parts[0] == "CANCEL":

        book.cancel_order(parts[1])

    else:

        order_id, side, price, qty = parts

        book.add_order(order_id, side, float(price), int(qty))


book.print_book()