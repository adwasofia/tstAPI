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