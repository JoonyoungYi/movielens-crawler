from sqlalchemy import Column, Integer, String, Date, Boolean
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from configs import *

engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
Base = declarative_base()


class Item(Base):
    __tablename__ = 'item'

    id = Column(Integer, nullable=False, primary_key=True)
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


# print(User.__table__)
# print(User.__mapper__)
#
# ed_user = User('haruair', 'Edward Kim', '1234')
# print(ed_user.name)  # 'haruair'
# print(ed_user.password)  # '1234'
# print(ed_user.id)  # 'None'
#
# Session = sessionmaker(bind=engine)
# # Session = sessionmaker()
# # Session.configure(bind=engine)
#
# session = Session()
# session.add(ed_user)
# session.commit()
#
# print(ed_user.id)
