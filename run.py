import codecs
import re
from datetime import datetime

from sqlalchemy import create_engine
from configs import *


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
    engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)

    from sqlalchemy.ext.declarative import declarative_base
    Base = declarative_base()

    from sqlalchemy import Column, Integer, String

    class User(Base):
        __tablename__ = 'users'

        id = Column(Integer, primary_key=True)
        name = Column(String(50))
        fullname = Column(String(50))
        password = Column(String(50))

        def __init__(self, name, fullname, password):
            self.name = name
            self.fullname = fullname
            self.password = password

        def __repr__(self):
            return "<User('%s', '%s', '%s')>" % (self.name, self.fullname,
                                                 self.password)

    # Base.metadata.create_all(engine)

    print(User.__table__)
    print(User.__mapper__)

    ed_user = User('haruair', 'Edward Kim', '1234')
    print(ed_user.name)  # 'haruair'
    print(ed_user.password)  # '1234'
    print(ed_user.id)  # 'None'

    from sqlalchemy.orm import sessionmaker
    Session = sessionmaker(bind=engine)
    # Session = sessionmaker()
    # Session.configure(bind=engine)

    session = Session()
    session.add(ed_user)
    session.commit()

    print(ed_user.id)

    Base.metadata.drop_all(engine)
