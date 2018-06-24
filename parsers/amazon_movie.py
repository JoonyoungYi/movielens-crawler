from traceback import format_exc

import re
import requests

from models import Session
from models import RottenMovie
from models import AmazonMovie
from models import WebPage


def main():
    session = Session()

    for idx, rotten_movie in enumerate(
            session.query(RottenMovie).filter(
                RottenMovie.amazon_movie_id.is_(None),
                RottenMovie.affiliate_amazon_valid.is_(True), )):
        # if rotten_movie.id < 1623:
        #     continue

        m = re.search('^http://www.amazon.com/gp/product/(?P<path>.*)$',
                      rotten_movie.affiliate_amazon_url)
        if not m:
            assert re.search('^http://www.amazon.com/gp/video/primesignup',
                             rotten_movie.affiliate_amazon_url)
            continue

        url = '/{}'.format(m.group('path'))
        print('>>', rotten_movie.id, url)

        amazon_movie = session.query(AmazonMovie).filter_by(url=url).first()
        if amazon_movie is None:
            amazon_movie = AmazonMovie(url=url)
            session.add(amazon_movie)

        rotten_movie.amazon_movie = amazon_movie
        if idx % 100 == 0:
            session.commit()
    session.commit()


if __name__ == '__main__':
    main()
