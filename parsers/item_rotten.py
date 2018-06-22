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


def __filter_movies_by_year(movies, valid_years, offset=2):
    if not valid_years:
        return []

    valid_years = [valid_years[0] - offset
                   ] + valid_years + [valid_years[-1] + offset]
    # 연도가 1년 차이나는 영화를 체크합니다.
    # 기존에는 연도가 정확한 걸 우선 체크하고 이 코드를 수행했으나,
    # 예외가 발생해 이렇게 하게 되었습니다.
    return [m for m in movies if m.get('year') and m['year'] in valid_years]


def __filter_movies_by_query(movies, query):
    return [m for m in movies if m['name'] == query]


def _select_movie(movies, query, valid_years):
    if len(movies) == 1:
        return movies[0]

    _movies = __filter_movies_by_year(movies, valid_years)
    if _movies:
        if len(_movies) == 1:
            return _movies[0]

        for m in _movies:
            if m['name'] == query:
                return m

        return _movies[0]

    _movies = __filter_movies_by_year(movies, valid_years, offset=3)
    # 이 때는 완벽하게 일치할 때만 진행합니다. 거기에 연도도 확인합니다.
    # 아닌 경우 불상사가 발생할 수 있습니다.
    for m in _movies:
        if m['name'] == query:
            return m

    # 연도에 맞는 영화가 없습니다.
    return None


def _request_movies_from_page(page, q, unit=100):
    q = re.sub('\'\s+', '', q)
    q = re.sub('\'', ' ', q)
    q = re.sub('\s+', ' ', q)
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
    # print(type(movies))
    movie = _select_movie(movies, query, valid_years)
    # print(movie)
    assert movie is None or type(movie) == dict
    return movie


def _get_movie(item):
    if not item.get_valid_years():
        return None
    # assert item.year

    main_name, sub_name = item.get_main_and_sum_names()
    valid_years = item.get_valid_years()

    if not sub_name:
        # 괄호가 없는 케이스를 핸들링합니다.
        movie = _request_movie(main_name, valid_years)
        if movie:
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
        if sub_movie and main_movie:
            main_similarity = ___get_str_similarity(main_movie['name'],
                                                    main_name)
            sub_similarity = ___get_str_similarity(sub_movie['name'], sub_name)
            if main_name == main_movie['name'] and sub_name != sub_movie['name']:
                return main_movie
            if main_name != main_movie['name'] and sub_name == sub_movie['name']:
                return sub_movie

            print(
                '   [*] Main:',
                '{:4f}'.format(main_similarity),
                main_movie['name'],
                main_movie['year'],
                main_movie['url'], )
            print(
                '   [*] Sub :',
                '{:4f}'.format(sub_similarity),
                sub_movie['name'],
                sub_movie['year'],
                sub_movie['url'], )

            raw = None
            while raw != 'm' and raw != 's' and raw != 'u':
                raw = input('Enter Main(m) / Sub(s) / Unknown(u) :')
                raw = raw.strip().lower()

            if raw == 'm':
                return main_movie
            elif raw == 's':
                return sub_movie

    # 결정된 사안이 없으면, keywords를 활용합니다.
    for keyword in item.get_rotten_keywords():
        movie = _request_movie(keyword, valid_years)
        if movie:
            return movie

    return None


def _save_movie_to_rotten_movie(session, movie, item):
    # print(movie)
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
    for idx, item in enumerate(
            session.query(Item).filter(Item.rotten_movie_id.is_(None))):
        if item.id < 1623:
            continue

        print(
            '\n>>',
            item.id,
            item.get_valid_years(),
            item.get_pretty_name(), )

        raw = None
        while raw != 'y' and raw != 'n':
            raw = input(
                'Want to input keyword? Enter, yes(y) / no(n): ').strip()

        if raw == 'y':
            keyword = None
            while not keyword:
                keyword = input('Enter Keyword: ').strip()
            item.rotten_keywords = keyword
            session.commit()

        movie = _get_movie(item)
        if movie is None:
            continue

        _save_movie_to_rotten_movie(session, movie, item)


if __name__ == '__main__':
    main()
