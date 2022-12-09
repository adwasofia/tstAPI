from pydantic import BaseModel

class Song(BaseModel):
    id: int
    track_name: str
    artist_name: str
    genre: str
    beats_per_minute: int
    popularity: int

class User(BaseModel):
    username: str
    password: str

class ShowSong(Song):
    pass