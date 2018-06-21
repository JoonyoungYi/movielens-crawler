import re
import json
# import hashlib
import time

import requests

from models import Session
from models import Item
from models import RottenMovie
from utils.item import get_query

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

    # for movie in movies:
    #     print(movie['name'], movie['year'])
    return __filter_movies_by_year(movies, item.release_date.year)


def _select_movie(movies, item):
    movies = __filter_movies(movies, item)
    if len(movies) == 0:
        # 연도에 맞는 영화가 없습니다.
        return None

    if len(movies) == 1:
        return movies[0]

    for m in movies:
        if m['name'] == item.name:
            return m
    return movies[0]


def _get_movies_from_page(page, q, unit=100):
    for i in range(10):
        r = requests.get(
            'https://www.rottentomatoes.com/api/private/v2.0/search',
            params={
                'q': q,
                't': 'movie',
                'offset': page * unit,
                'limit': unit,
            })
        try:
            data = r.json()
        except:
            print(r.url)
            print(r.text)

            assert False
        movies = data.get('movies')
        movie_number = data.pop('movieCount')
        # print('>>', page, len(movies), movie_count)
        if movie_number == 0:
            return [], 0
        if movies:
            return movies, movie_number
    return None, None


def _get_movies(item):
    query = get_query(item.name)
    movies, movie_number, unit = [], 0, 30
    for page in range(1000):
        _movies, _movie_number = _get_movies_from_page(page, query, unit=unit)
        movie_number = max(_movie_number, movie_number)
        if _movies is None:
            break
        movies.extend(_movies)
        print('   [*]', page, len(_movies), movie_number)

        if unit * (page + 1) > movie_number:
            break
        time.sleep(0.25)
    return movies


def _get_movie(item):
    if item.year is None:
        return None
    # assert item.year

    movies = _get_movies(item)
    # print('   [*]', len(movies))
    if len(movies) == 0:
        # 검색 결과 없음.
        return None

    movie = _select_movie(movies, item)
    if movie is None:
        return None

    return movie


def _save_movie_to_rotten_movie(session, movie, item):
    name = movie.pop('name', '')
    year = movie.pop('year', '')
    url = movie.pop('url', '')
    print(item.year, item.name)
    print(year, name)

    rotten_movie = session.query(RottenMovie).filter_by(
        name=name, year=year, url=url).first()
    if rotten_movie is None:
        rotten_movie = RottenMovie(
            name=name, year=year, url=url, data=json.dumps(movie))
        session.add(rotten_movie)
    item.rotten_movie = rotten_movie
    session.commit()


def main():
    session = Session()
    for i, item in enumerate(session.query(Item)):
        # if i <= 1437:
        #     continue

        print('\n>>', i, item.release_date.year, item.name)
        movie = _get_movie(item)
        if movie is None:
            continue

        _save_movie_to_rotten_movie(session, movie, item)


if __name__ == '__main__':
    main()
