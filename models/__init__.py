import re
from datetime import datetime

from sqlalchemy import Column, ForeignKey
from sqlalchemy import Boolean, Text, Integer, String, Date, DateTime
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from configs import *
from utils import generator

engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)

# Session = sessionmaker()
# Session.configure(bind=engine)


class Item(Base):
    __tablename__ = 'item'

    DATASET_MOVIELENS_100K = 'ml_100k'

    id = Column(Integer, nullable=False, primary_key=True)
    dataset = Column(String(10), index=True, default='')
    key = Column(String(10), index=True, default='')

    name = Column(String(150), index=True, default='')
    year = Column(Integer, index=True)
    rotten_keywords = Column(String(1000), default='')

    release_date = Column(Date, index=True)
    video_release_date = Column(Date)

    old_imdb_url = Column(String(1000), default='')

    category_action = Column(Boolean, default=False, nullable=False)
    category_adventure = Column(Boolean, default=False, nullable=False)
    category_animation = Column(Boolean, default=False, nullable=False)
    category_children = Column(Boolean, default=False, nullable=False)
    category_comedy = Column(Boolean, default=False, nullable=False)
    category_crime = Column(Boolean, default=False, nullable=False)
    category_documentary = Column(Boolean, default=False, nullable=False)
    category_drama = Column(Boolean, default=False, nullable=False)
    category_fantasy = Column(Boolean, default=False, nullable=False)
    category_flim_noir = Column(Boolean, default=False, nullable=False)
    category_horror = Column(Boolean, default=False, nullable=False)
    category_musical = Column(Boolean, default=False, nullable=False)
    category_mystery = Column(Boolean, default=False, nullable=False)
    category_romance = Column(Boolean, default=False, nullable=False)
    category_sci_fi = Column(Boolean, default=False, nullable=False)
    category_thriller = Column(Boolean, default=False, nullable=False)
    category_war = Column(Boolean, default=False, nullable=False)
    category_western = Column(Boolean, default=False, nullable=False)

    # Relation
    rotten_movie_id = Column(
        Integer,
        ForeignKey('rotten_movie.id'),
        nullable=True, )
    original_item_id = Column(Integer, index=True, nullable=True)

    def get_valid_years(self, offset=0):
        if self.year and self.release_date:
            min_year = min(self.year, self.release_date.year)
            max_year = max(self.year, self.release_date.year)
            return list(range(min_year - offset, max_year + 1 + offset))
        return []

    def is_valid_year(self, year, offset=0):
        return year in self.get_valid_years(offset=offset)

    def _handle_last_comma(name):
        m = re.search('^(?P<l>.*), (?P<r>[0-9a-zA-Z\']+)$', name.strip())
        if m:
            return '{} {}'.format(m.group('r'), m.group('l')).strip()
        else:
            return name.strip()

    def get_main_and_sum_names(self):
        m = re.search('(?P<main>.*)\s*\((?P<sub>.*)\)\s*$', self.name)
        if m:
            main = m.group('main')
            sub = m.group('sub')
            # print(main, sub)
            return Item._handle_last_comma(main), Item._handle_last_comma(sub)
        else:
            return Item._handle_last_comma(self.name), None

    def get_pretty_name(self):
        main_name, sub_name = self.get_main_and_sum_names()
        if sub_name:
            return '{} ({})'.format(main_name, sub_name)
        else:
            return main_name

    def get_rotten_keywords(self):
        if self.rotten_keywords:
            return [k.strip() for k in self.rotten_keywords.split('|')]
        return []


class RottenMovie(Base):
    __tablename__ = 'rotten_movie'

    id = Column(Integer, nullable=False, primary_key=True)

    name = Column(String(150), index=True, default='')
    year = Column(Integer, index=True)
    url = Column(String(150), index=True, default='')

    data = Column(Text, default='')

    # Relation
    items = relationship('Item', backref='rotten_movie', lazy='dynamic')
    web_page_id = Column(
        Integer,
        ForeignKey('web_page.id'),
        nullable=True, )


class WebPage(Base):
    __tablename__ = 'web_page'

    id = Column(Integer, nullable=False, primary_key=True)
    key = Column(String(128), index=True, default=generator.generate_128_key)
    parsed_datetime = Column(DateTime, default=datetime.now)
