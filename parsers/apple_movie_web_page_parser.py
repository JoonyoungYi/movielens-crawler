from traceback import format_exc
import re

import requests
from bs4 import BeautifulSoup

from models import Session
from models import AppleMovie
from models import WebPage


def _get_soup_from_apple_movie(apple_movie):
    with open('cdn/{}.html'.format(apple_movie.web_page.key), 'r') as f:
        soup = BeautifulSoup(f.read(), "html5lib")
        return soup
    return None


def _get_price_from_soup(soup):
    content = soup.find('div', {'id': 'content'})
    if not content:
        return None

    left_stack = content.find('div', {'id': 'left-stack'})
    if not left_stack:
        return None

    div = left_stack.find('div', 'movie', recursive=False)
    if not div:
        return None

    ul = div.find('ul', 'list', recursive=False)
    if not ul:
        return None

    span = ul.find('span', 'price')
    if not span:
        return None

    span = span.find('span', {'itemprop': "price"})
    if not span:
        return None

    m = re.search('^\$(?P<p>\d+\.\d+)$', span.get('content'))
    if m:
        return float(m.group('p'))

    return None


def main():
    session = Session()

    for idx, apple_movie in enumerate(
            session.query(AppleMovie).filter(
                AppleMovie.web_page_id.isnot(None),
                AppleMovie.price.is_(None), )):
        # if apple_movie.id < 434:
        #     continue

        print(
            '>>',
            '{:4d}'.format(apple_movie.id), )
        soup = _get_soup_from_apple_movie(apple_movie)
        if soup is None:
            raise NotImplementedError()
            continue

        price = _get_price_from_soup(soup)
        if not price:
            continue
            
        apple_movie.price = price

        if idx % 100 == 0:
            session.commit()

    session.commit()


if __name__ == '__main__':
    main()
