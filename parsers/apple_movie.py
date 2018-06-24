from traceback import format_exc

import re
import requests

from models import Session
from models import RottenMovie
from models import AppleMovie
from models import WebPage


def main():
    session = Session()

    for idx, rotten_movie in enumerate(
            session.query(RottenMovie).filter(
                RottenMovie.apple_movie_id.is_(None),
                RottenMovie.affiliate_apple_valid.is_(True), )):
        # if rotten_movie.id < 1623:
        #     continue

        m = re.search('https://itunes.apple.com/us/movie/(?P<path>.*)$',
                      rotten_movie.affiliate_apple_url)
        assert m
        url = '/{}'.format(m.group('path'))
        print('>>', rotten_movie.id, url)

        apple_movie = session.query(AppleMovie).filter_by(url=url).first()
        if apple_movie is None:
            apple_movie = AppleMovie(url=url)
            session.add(apple_movie)

        rotten_movie.apple_movie = apple_movie

        if idx % 100 == 0:
            session.commit()
    session.commit()


if __name__ == '__main__':
    main()
