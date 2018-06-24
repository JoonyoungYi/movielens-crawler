from traceback import format_exc

import requests
from bs4 import BeautifulSoup

from models import Session
from models import RottenMovie
from models import WebPage


def _get_soup_from_rotten_movie(rotten_movie):
    with open('cdn/{}.html'.format(rotten_movie.web_page.key), 'r') as f:
        soup = BeautifulSoup(f.read(), "html5lib")
        return soup
    return None


def main():
    session = Session()

    for idx, rotten_movie in enumerate(
            session.query(RottenMovie).filter(
                RottenMovie.web_page_id.isnot(None))):
        # if rotten_movie.id < 434:
        #     continue

        print(
            '>>',
            '{:4d}'.format(rotten_movie.id), )
        soup = _get_soup_from_rotten_movie(rotten_movie)
        if soup is None:
            raise NotImplementedError()
            continue

        movie_divs = soup.find_all('div', 'movie_links')
        if len(movie_divs) > 1:
            print(len(movie_divs))
            raise NotImplementedError()

        if len(movie_divs) <= 0:
            continue

        for a_tag in movie_divs[0].find_all('a', recursive=False):
            div = a_tag.find('div', recursive=False)
            div_id = div['id']
            if div_id not in ("amazonAffiliates", 'itunesAffiliates',
                              'FandangoNow', 'vuduAffiliates',
                              'netflixAffiliates', ):
                print(div_id)
                raise NotImplementedError()

        # break


if __name__ == '__main__':
    main()
