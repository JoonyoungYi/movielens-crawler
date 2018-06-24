from traceback import format_exc
import time
import random
import urllib.parse

import requests
from bs4 import BeautifulSoup

from models import Session
from models import AmazonMovie
from models import WebPage
from utils.cdn import save_to_cdn


def __request(path):
    s = requests.Session()
    s.headers.update({
        'accept':
        'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding':
        'gzip, deflate, br',
        'accept-language':
        'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6,zh;q=0.5',
        'cache-control':
        'no-cache',
        'pragma':
        'no-cache',
        'upgrade-insecure-requests':
        '1',
        'user-agent':
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
    })

    try:
        r = s.get('https://www.amazon.com/gp/product{}'.format(path))
        text = r.text
        # soup = BeautifulSoup(text, "html5lib")
        # print(soup.prettify())
        return text
    except:
        print(format_exc())
        return None


def __save(key, text):
    return save_to_cdn(key, text)


def _request_and_save(key, path):
    text = __request(path)
    print(path)
    # assert False
    if not text:
        return False

    return __save(key, text)


def main():
    session = Session()
    for idx, amazon_movie in enumerate(
            session.query(AmazonMovie).filter(
                AmazonMovie.web_page_id.is_(None))):
        # time.sleep(1)
        # if amazon_movie.id < 1623:
        #     continue

        print(
            '>>',
            '{:4d}'.format(amazon_movie.id), )
        if not amazon_movie.url:
            continue

        web_page = WebPage()
        session.add(web_page)
        amazon_movie.web_page = web_page
        session.commit()

        success = _request_and_save(web_page.key, amazon_movie.url)
        if not success:
            session.delete(web_page)
            amazon_movie.web_page = None
            session.commit()
            print('  [-] Fail')
        else:
            print('  [+] Success')

        # break


if __name__ == '__main__':
    main()
