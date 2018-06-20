import re
import json
# import hashlib

import requests
from bs4 import BeautifulSoup

from models import Item
from models import Session


def _get(url, **kwargs):
    r = requests.get(url, **kwargs)
    # key = hashlib.sha512(r.url.encode('utf-8')).hexdigest()
    # assert len(key) <= 128
    # url = r.url
    return r


def _handle_item(item):
    # if item.year is None:
    #     return None
    assert item.year

    r = _get(
        'https://www.rottentomatoes.com/search/',
        params={
            'search': item.name,
        })
    soup = BeautifulSoup(r.text, "html5lib")
    # print(r.text)
    div = soup.find('div', {'id': 'main_container'})
    # div = div.find('div', {'id':'search-results-root'})
    scripts = div.find_all('script')
    if len(scripts) < 2:
        return None

    script = scripts[0]
    script = script.get_text().strip()
    script = re.sub('\s+', ' ', script)
    # print(script)

    m = re.search(
        'RT.PrivateApiV2FrontendHost, \'(?P<name>.*)\', (?P<dict>.*)\); }\);',
        script)
    assert m
    name = m.group('name')
    d = json.loads(m.group('dict'))

    if item.year is not None:
        movies = []
        for movie in d.get('movies', []):
            year = movie.get('year', None)
            if year is None:
                continue
            if year == item.year:
                movies.append(movie)

        if len(movies) == 0:
            for movie in d.get('movies', []):
                year = movie.get('year', None)
                if year is None:
                    continue
                if item.year - 1 <= year <= item.year + 1:
                    movies.append(movie)
    else:
        movies = []

    if len(movies) == 0:
        if len(d.get('movies', [])) == 1:
            movies = d.get('movies', [])

    assert movies

    movie = None
    for m in movies:
        if m['name'] == item.name:
            moive = m

    if movie is None:
        movie = movies[0]

    print(item.year, item.name)
    print(movie)
    print(movie['year'], movie['name'])

    # assert m

    # ul = section.find('ul', 'results_ul')
    # for li in ul.find_all('li', recursive=False):
    #     print(li.prettify())


def main():
    session = Session()
    for i, item in enumerate(session.query(Item)):
        if i <= 106:
            continue

        print('>>', i, item.year, item.name)
        _handle_item(item)
        # break
        input('Enter:')


if __name__ == '__main__':
    main()
