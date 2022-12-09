from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import schemas, models, hashing
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from typing import List
from .hashing import Hash

app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/song', status_code=status.HTTP_201_CREATED)
def create_song (request : schemas.Song, db : Session = Depends(get_db)):
    new_song = models.Song(track_name=request.track_name, artist_name=request.artist_name, genre=request.genre, beats_per_minute=request.beats_per_minute, popularity=request.popularity)
    db.add(new_song)
    db.commit()
    db.refresh(new_song)
    return new_song

@app.post('/user', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowUser)
def create_user (request : schemas.User, db : Session = Depends(get_db)):
    
    new_user = models.User(username=request.username, password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get('/user/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowUser)
def get_user_by_id (id, response : Response, db : Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'User with id {id} does not exist')
    return user

@app.get('/song', status_code=status.HTTP_200_OK, response_model=List[schemas.ShowSong])
def get_all_songs (db : Session = Depends(get_db)):
    songs = db.query(models.Song).all()
    if not songs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'There is no song in the database.')
    return songs

@app.get('/song/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowSong)
def get_song_by_id (id, response : Response, db : Session = Depends(get_db)):
    song = db.query(models.Song).filter(models.Song.id == id).first()
    if not song:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'Song with id {id} does not exist')
    return song

@app.get('/recs/{weather}', status_code=status.HTTP_200_OK)
def get_recs (weather, db : Session = Depends(get_db)):
    if (weather == 'sunny'):
        songs = db.query(models.Song).filter(models.Song.beats_per_minute > 100).order_by(models.Song.popularity.desc()).all()
    elif (weather == 'rainy'):
        songs = db.query(models.Song).filter(models.Song.beats_per_minute <= 100).order_by(models.Song.popularity.desc()).all()
    else:
        songs = 'Silakan ulangi input.'
    return songs