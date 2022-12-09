from typing import Optional
from pydantic import BaseModel

class Song(BaseModel):
    track_name: str
    artist_name: str
    genre: str
    beats_per_minute: int
    popularity: int

class User(BaseModel):
    username: str
    password: str

class ShowSong(BaseModel):
    track_name: str
    artist_name: str
    class Config():
        orm_mode = True

class ShowUser(BaseModel):
    username: str
    class Config():
        orm_mode = True

class Login(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None