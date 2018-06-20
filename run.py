import codecs
import re
from datetime import datetime


def _extract_name_and_year(text):
    m = re.search('^(?P<name>.*)\s*\((?P<year>\d{4})\)$', text)
    if m:
        return m.group('name').strip(), int(m.group('year'))
    elif key == '267':
        assert text == 'unknown'
        return 'unknown', None
    elif key == '1412':
        assert text == 'Land Before Time III: The Time of the Great Giving (1995) (V)'
        return 'Land Before Time III: The Time of the Great Giving', 1995
    return None, None


def _get_date(text):
    if not text:
        return None
    datetime_value = datetime.strptime(text, '%d-%b-%Y')
    return datetime_value.date()


def main():
    f = codecs.open('data/u.item', 'r', 'utf-8', 'ignore')
    for line in f:
        cols = [c.strip() for c in line.strip().split('|')]
        assert len(cols) == 24

        key = cols[0]
        # print(key)

        name, year = _extract_name_and_year(cols[1])
        if name is None:
            raise Exception('Can\'t split name and year from 2nd column')
        # print(name, year)

        release_date = _get_date(cols[2])
        # print(release_date)

        video_release_date = _get_date(cols[3])
        # print(video_release_date)

        old_imdb_url = cols[4]
        # print(old_imdb_url)

        # category가 unknown인 경우, 다른 valid한 category가 없어야 합니다.
        if cols[5] == '1':
            assert sum(int(d) for d in cols[6:]) == 0

        for j, key in zip(
                range(6, 24), [
                    'action', 'adventure', 'animation', 'children', 'comedy',
                    'crime', 'documentary', 'drama', 'fantasy', 'flim_noir',
                    'horror', 'musical', 'mystery', 'romance', 'sci_fi',
                    'thriller', 'war', 'western'
                ]):
            bool_value = (int(cols[j]) == 1)
            # print('category_{}'.format(key), bool_value)


if __name__ == '__main__':
    # main()

    # main2()


    # Base.metadata.drop_all(engine)
