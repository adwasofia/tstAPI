from sqlalchemy import Column, Integer, String
from .database import Base

class Song(Base):
    __tablename__ = 'songs'
    id = Column(Integer, primary_key=True, index=True)
    track_name = Column(String)
    artist_name = Column(String)
    genre = Column(String)
    beats_per_minute = Column(Integer)
    popularity = Column(Integer)

class User(Base):
    __tablename__ = 'users'
    username = Column(String, primary_key=True, index=True)
    password = Column(String)
