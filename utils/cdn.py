import os
import re
from traceback import format_exc

from bs4 import BeautifulSoup


def get_soup_from_web_page(web_page):
    try:
        dir, filename = _extract_dir(web_page.key)
        # print(web_page.key)
        # print(len(dir), len(filename))
        with open('cdn/{}/{}.html'.format(dir, filename), 'r') as f:
            soup = BeautifulSoup(f.read(), "html5lib")
            return soup
    except:
        # print(format_exc())
        pass
    return None


def _extract_dir(key):
    return key[:2].lower(), key[2:]


def _make_dir(dir):
    path = 'cdn/{}'.format(dir)
    if not os.path.exists(path):
        os.mkdir(path)


def save_to_cdn(key, text):
    dir, filename = _extract_dir(key)
    _make_dir(dir)
    filepath = 'cdn/{}/{}.html'.format(dir, filename)
    with open(filepath, 'w') as f:
        f.write(text)
        # print('success', filepath, key)
        f.close()
        return True
    return False


def __make_directories():
    for filename in os.listdir('cdn/'):
        dir = 'cdn/{}'.format(filename)
        if os.path.isdir(dir):
            os.rename(dir, "cdn/{}".format(filename.lower()))
            # for filename in os.listdir(dir):
            #     m = re.search('^(?P<key>.*)\.html$', filename)
            #     if not m:
            #         continue
            #
            #     filepath = '{}/{}'.format(dir, filename)
            #
            #     print(filename)
            #     _key = m.group('key')
            #     dir, key = _extract_dir(_key)
            #     _make_dir(dir)

                # assert m


if __name__ == '__main__':
    __make_directories()
