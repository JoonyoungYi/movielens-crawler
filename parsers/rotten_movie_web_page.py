from traceback import format_exc

import requests

from models import Session
from models import RottenMovie
from models import WebPage
from utils.cdn import save_to_cdn


def __request(path):
    try:
        r = requests.get('https://www.rottentomatoes.com{}'.format(path))
        return r.text
    except:
        print(format_exc())
        return None


def __save(key, text):
    return save_to_cdn(key, text)


def _request_and_save(key, path):
    text = __request(path)
    if not text:
        return False

    return __save(key, text)


def main():
    session = Session()

    for idx, rotten_movie in enumerate(
            session.query(RottenMovie).filter(
                RottenMovie.web_page_id.is_(None))):
        # if rotten_movie.id < 1623:
        #     continue

        print(
            '>>',
            '{:4d}'.format(rotten_movie.id), )
        if not rotten_movie.url:
            continue

        web_page = WebPage()
        session.add(web_page)
        rotten_movie.web_page = web_page
        session.commit()

        success = _request_and_save(web_page.key, rotten_movie.url)
        if not success:
            session.delete(web_page)
            rotten_movie.web_page = None
            session.commit()
            print('  [-] Fail')
        else:
            print('  [+] Success')

        # break


if __name__ == '__main__':
    main()
