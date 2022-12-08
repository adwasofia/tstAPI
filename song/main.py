from fastapi import FastAPI, Depends
from . import schemas
from . import models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/song')
def create(request : schemas.Song, db : Session = Depends(get_db)):
    new_song = models.Song(id=request.id, track_name=request.track_name, artist_name=request.artist_name, genre=request.genre, beats_per_minute=request.beats_per_minute, popularity=request.popularity)
    db.add(new_song)
    db.commit()
    db.refresh(new_song)
    return new_song

@app.post('/user')
def create(request : schemas.User, db : Session = Depends(get_db)):
    new_user = models.User(username=request.username, password=request.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get('/song')
def all(db : Session = Depends(get_db)):
    songs = db.query(models.Song).all()
    return songs

@app.get('/recs/{weather}')
def get_recs (weather, db : Session = Depends(get_db)):
    if (weather == 'sunny'):
        songs = db.query(models.Song).filter(models.Song.beats_per_minute > 100).order_by(models.Song.popularity.desc()).all()
    elif (weather == 'rainy'):
        songs = db.query(models.Song).filter(models.Song.beats_per_minute <= 100).order_by(models.Song.popularity.desc()).all()
    else:
        songs = 'Silakan ulangi input.'
    return songs