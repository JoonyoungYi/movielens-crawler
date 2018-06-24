from traceback import format_exc

import requests
from bs4 import BeautifulSoup

from models import Session
from models import RottenMovie
from models import WebPage
from utils.cdn import get_soup_from_web_page


def _get_soup_from_rotten_movie(rotten_movie):
    return get_soup_from_web_page(rotten_movie.web_page)


def _get_affiliate_url(movie_div, div_id):
    for a_tag in movie_div.find_all('a', recursive=False):
        div = a_tag.find('div', recursive=False)
        assert div['id'] in ("amazonAffiliates", 'itunesAffiliates',
                             'FandangoNow', 'vuduAffiliates',
                             'netflixAffiliates', )
        if div['id'] == div_id:
            return a_tag['href']
    return None


def main():
    session = Session()

    for idx, rotten_movie in enumerate(
            session.query(RottenMovie).filter(
                RottenMovie.web_page_id.isnot(None))):
        if rotten_movie.id < 434:
            continue

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
        movie_div = movie_divs[0]

        for keyword, div_id in [
            ('amazon', "amazonAffiliates"),
            ('apple', 'itunesAffiliates'),
            ('fandangonow', 'FandangoNow'),
            ('vudu', 'vuduAffiliates'),
            ('netflix', 'netflixAffiliates', ),
        ]:
            prefix = 'affiliate_{}'.format(keyword)
            valid_column_name = '{}_valid'.format(prefix)
            url_column_name = '{}_url'.format(prefix)

            affiliate_url = _get_affiliate_url(movie_div, div_id)
            if affiliate_url:
                setattr(rotten_movie, valid_column_name, True)
                setattr(rotten_movie, url_column_name, affiliate_url)
            else:
                setattr(rotten_movie, valid_column_name, False)
                setattr(rotten_movie, url_column_name, '')

        session.commit()


if __name__ == '__main__':
    main()
