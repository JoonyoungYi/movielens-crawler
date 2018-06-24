from traceback import format_exc

import re
import requests

from models import Session
from models import Item


def main():
    session = Session()

    for idx, item in enumerate(
            session.query(Item).filter(
                Item.price.is_(None),
                Item.rotten_movie_id.isnot(None), )):
        # if rotten_movie.id < 1623:
        #     continue

        print(">>", item.id)

        rotten_movie = item.rotten_movie
        if not rotten_movie:
            continue

        amazon_movie = rotten_movie.amazon_movie
        apple_movie = rotten_movie.apple_movie
        if not apple_movie and not amazon_movie:
            continue

        prices = []
        if amazon_movie:
            prices.append(amazon_movie.get_price())
        if apple_movie:
            prices.append(apple_movie.price)
        prices = [p for p in prices if p and p > 0.0]
        if not prices:
            continue

        price = sum(prices) / len(prices)
        item.price = price

        if idx % 100 == 0:
            session.commit()
    session.commit()


if __name__ == '__main__':
    main()
