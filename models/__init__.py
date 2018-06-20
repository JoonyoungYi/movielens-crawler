from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from configs import *

engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
Base = declarative_base()


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
