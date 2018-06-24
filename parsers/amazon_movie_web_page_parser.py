from traceback import format_exc
import re
import time

import requests
from bs4 import BeautifulSoup

from models import Session
from models import AmazonMovie
from models import WebPage
from utils.cdn import get_soup_from_web_page


def _get_soup_from_amazon_movie(amazon_movie):
    return get_soup_from_web_page(amazon_movie.web_page)


def __get_price_from_form(form):
    div = form.find('div', 'dv-button-text')
    if not div:
        return None

    price_str = div.get_text().strip()
    if not price_str:
        return None

    m = re.search('\$(?P<p>\d+\.\d+)$', price_str)
    if m:
        return float(m.group('p'))
    return None


def __get_key_from_m(m):
    hs = m.group('hs')

    if m.group('br') == 'est':
        br = 'buy'
    else:
        br = 'rent'

    return '{}_{}_price'.format(hs, br)


def _get_price_dict_from_soup(soup):
    d = {}
    for form in soup.find_all('form', 'dv-action-single'):
        input_tag = form.find('input', {'name': 'reftag'})
        ref_tag = input_tag['value']

        m = re.search(
            'atv_dp_bb_(?P<br>(est|vod))_(?P<hs>(hd|sd))_movie_(ab|mw)',
            ref_tag)
        if not m:
            print(ref_tag)
            raise NotImplementedError()

        key = __get_key_from_m(m)
        value = d.get(key, None)
        if value is None:
            value = __get_price_from_form(form)
            d[key] = value
        else:
            assert value == __get_price_from_form(form)
    return d


def main():
    session = Session()

    for idx, amazon_movie in enumerate(
            session.query(AmazonMovie).filter(
                AmazonMovie.web_page_id.isnot(None),
                AmazonMovie.hd_buy_price.is_(None),
                AmazonMovie.sd_buy_price.is_(None),
                AmazonMovie.hd_rent_price.is_(None),
                AmazonMovie.sd_rent_price.is_(None), )):
        # if amazon_movie.id < 583:
        #     continue

        print(
            '>>',
            '{:4d}'.format(amazon_movie.id), )
        soup = _get_soup_from_amazon_movie(amazon_movie)
        if soup is None:
            print('  [-] File Not Found')
            # session.delete(amazon_movie.web_page)
            # amazon_movie.web_page_id = None
            continue

        price_dict = _get_price_dict_from_soup(soup)
        # print(price_dict)
        if not price_dict:
            print('  [-] Fail')
            session.delete(amazon_movie.web_page)
            amazon_movie.web_page_id = None
            continue

        print('  [+] Success', len(price_dict.items()))
        for key, value in price_dict.items():
            setattr(amazon_movie, key, value)

        if idx % 100 == 0:
            session.commit()

    session.commit()


if __name__ == '__main__':
    main()
