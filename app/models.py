from .database import Base
from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, text
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class Url(Base):
    __tablename__ = 'urls'

    id = Column(Integer, primary_key=True, nullable=False)
    long = Column(String, nullable=False)
    short = Column(String, nullable=False, unique=True)
    created = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    last_clicked = Column(TIMESTAMP(timezone=True))
    click_count = Column(Integer, nullable=False, default=0)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=True)


class Visit(Base):
    __tablename__ = 'visits'

    id = Column(Integer, primary_key=True, nullable=False)
    client_host = Column(String)
    headers = Column(String)
    time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    url_id = Column(Integer, ForeignKey('urls.id', ondelete='CASCADE'), nullable=False)