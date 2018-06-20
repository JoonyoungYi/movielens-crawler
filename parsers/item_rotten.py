import re
import json
# import hashlib
import time

import requests

from models import Session
from models import Item
from models import RottenMovie

# key = hashlib.sha512(r.url.encode('utf-8')).hexdigest()
# assert len(key) <= 128
# url = r.url


def __filter_movies_by_year(movies, year):
    if year is None:
        return []

    _movies = [m for m in movies if m.get('year') and m['year'] == year]
    # 연도가 정확하게 일치하는 영화를 체크합니다.
    if not _movies:
        # 연도가 1년 차이나는 영화를 체크합니다.
        _movies = [
            m for m in movies
            if m.get('year') and (year - 1 <= m['year'] <= year + 1)
        ]
    return _movies


def __filter_movies(movies, item):
    if len(movies) == 1:
        return movies

    return __filter_movies_by_year(movies, item.year)


def _select_movie(movies, item):
    movies = __filter_movies(movies, item)
    assert movies
    if len(movies) == 1:
        return movies[0]

    for m in movies:
        if m['name'] == item.name:
            return m
    return movies[0]


def _get_query(name):
    m = re.search('^(?P<l>.*), (?P<r>[0-9a-zA-Z]+)$', name)
    if m:
        return m.group('r') + ' ' + m.group('l')
    else:
        return name


def _get_movies_from_page(s, page, q):
    for i in range(10):
        r = s.get(
            'https://www.rottentomatoes.com/api/private/v2.0/search',
            params={
                'q': q,
                't': 'movie',
                'offset': page * 30,
                'limit': 30,
            })
        print(r.url)
        data = r.json()
        movies = data.get('movies')
        if data.pop('movieCount') == 0:
            return []

        if movies:
            return movies
        else:
            print(data)


def _get_movies(item):
    s = requests.Session()
    s.get('https://www.rottentomatoes.com/search/')

    movies = []
    for page in range(1000):
        _movies = _get_movies_from_page(s, page, _get_query(item.name))
        movies.extend(_movies)
        print('..', page, len(_movies))
        if not _movies:
            break

        time.sleep(1)
    # assert False
    return movies


def _get_rotten_movie(item):
    if item.year is None:
        return None
    # assert item.year

    movies = _get_movies(item)
    print(len(movies))
    assert len(movies) < 1000

    movie = _select_movie(movies, item)
    if movie is None:
        return None

    print(item.year, item.name)
    name = movie.pop('name', '')
    year = movie.pop('year', '')
    url = movie.pop('url', '')
    print(year, name)

    rotten_movie = RottenMovie(
        name=name, year=year, url=url, data=json.dumps(movie))
    return rotten_movie


def main():
    session = Session()
    for i, item in enumerate(session.query(Item)):
        if i <= 331:
            continue

        print('\n>>', i, item.year, item.name)
        rotten_movie = _get_rotten_movie(item)
        if rotten_movie is None:
            continue

        session.add(rotten_movie)
        item.rotten_movie = rotten_movie
        session.commit()


if __name__ == '__main__':
    main()
