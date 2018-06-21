import re
import json
# import hashlib
import time
from difflib import SequenceMatcher

import requests

from models import Session
from models import Item
from models import RottenMovie

# key = hashlib.sha512(r.url.encode('utf-8')).hexdigest()
# assert len(key) <= 128
# url = r.url


def ___get_str_similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()


def __filter_movies_by_year(movies, valid_years):
    if not valid_years:
        return []

    # 연도가 정확하게 일치하는 영화를 체크합니다.
    _movies = [m for m in movies if m.get('year') and m['year'] in valid_years]

    if not _movies:
        offset = 1
        valid_years = [valid_years[0] - offset
                       ] + valid_years + [valid_years[-1] + offset]
        # 연도가 1년 차이나는 영화를 체크합니다.
        _movies = [
            m for m in movies if m.get('year') and m['year'] in valid_years
        ]
    return _movies


def __filter_movies(movies, valid_years):
    if len(movies) == 1:
        return movies

    return __filter_movies_by_year(movies, valid_years)


def _select_movie(movies, query, valid_years):
    movies = __filter_movies(movies, valid_years)
    if len(movies) == 0:
        # 연도에 맞는 영화가 없습니다.
        return None

    if len(movies) == 1:
        return movies[0]

    for m in movies:
        if m['name'] == query:
            return m

    return movies[0]


def _request_movies_from_page(page, q, unit=100):
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


def _request_movies_by_query(query):
    movies, movie_number, unit = [], 0, 30
    for page in range(1000):
        _movies, _movie_number = _request_movies_from_page(
            page, query, unit=unit)
        movie_number = max(_movie_number, movie_number)
        if _movies is None:
            break
        movies.extend(_movies)
        print('   [*]', page, len(_movies), movie_number)

        if unit * (page + 1) > movie_number:
            break
        time.sleep(0.25)
    return movies


def _request_movie(query, valid_years):
    movies = _request_movies_by_query(query)
    return _select_movie(movies, query, valid_years)


def _get_movie(item):
    if not item.get_valid_years():
        return None
    # assert item.year

    main_name, sub_name = item.get_main_and_sum_names()
    valid_years = item.get_valid_years()
    if not sub_name:
        # 괄호가 없는 케이스를 핸들링합니다.
        movie = _request_movie(main_name, valid_years)
        return movie
    else:
        movie = _request_movie('{} ({})'.format(main_name, sub_name),
                               valid_years)
        if movie:
            return movie

        movie = _request_movie('{} ({})'.format(sub_name, main_name),
                               valid_years)
        if movie:
            return movie

        main_movie = _request_movie(main_name, valid_years)
        sub_movie = _request_movie(sub_name, valid_years)
        if main_movie and not sub_movie:
            return main_movie
        if sub_movie and not main_movie:
            return sub_movie
        if not sub_movie and not main_movie:
            return None

        main_similarity = ___get_str_similarity(main_movie['name'], main_name)
        sub_similarity = ___get_str_similarity(sub_movie['name'], sub_name)
        print(
            '   [*] Main:',
            '{:4f}'.format(main_similarity),
            main_movie['name'], )
        print(
            '   [*] Sub :',
            '{:4f}'.format(sub_similarity),
            sub_movie['name'], )

        input('Enter:')
        if abs(main_similarity - sub_similarity) > 0.5:
            if main_similarity > sub_similarity:
                return main_movie
            else:
                return sub_movie

        raise NotImplementedError()


def _save_movie_to_rotten_movie(session, movie, item):
    name = movie.pop('name', '')
    year = movie.pop('year', '')
    url = movie.pop('url', '')
    print(item.year, item.get_pretty_name())
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
    for idx, item in enumerate(session.query(Item)):
        if idx <= 1095:
            continue

        print(
            '\n>>',
            idx,
            item.get_valid_years(),
            item.get_pretty_name(), )
        movie = _get_movie(item)
        if movie is None:
            continue

        _save_movie_to_rotten_movie(session, movie, item)


if __name__ == '__main__':
    main()
