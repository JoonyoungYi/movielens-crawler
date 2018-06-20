from sqlalchemy import Column, Integer, String, Date, Boolean
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from configs import *

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


class RottenMovie(Base):
    __tablename__ = 'rotten_movie'

    id = Column(Integer, nullable=False, primary_key=True)

    name = Column(String(150), index=True, default='')
    year = Column(Integer, index=True)
    url = Column(String(150), index=True, default='')

    data = Column(String(2000), default='')
