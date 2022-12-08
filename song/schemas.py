from pydantic import BaseModel

class Song(BaseModel):
    title: str
    bpm: int