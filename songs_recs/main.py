from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import schemas, models, jwtToken, oAuth2
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from typing import List
from .hashing import Hash
from fastapi.security import OAuth2PasswordRequestForm

app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db : Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == request.username).first()
    if (not user):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'Login failed (username does not exist).')
    if (not Hash.verify(request.password, user.password)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'Login failed (incorrect password).')
    
    # Menghasilkan token jwt
    access_token = jwtToken.create_access_token(
        data={"sub": user.username}
    )
    return {"access_token": access_token, "token_type": "bearer"}

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
def get_user_by_id (id, response : Response, db : Session = Depends(get_db), get_current_user:schemas.User = Depends(oAuth2.get_current_user)):
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
    if (weather == 'cloudy'):
        songs = db.query(models.Song).filter(models.Song.beats_per_minute <= 110).order_by(models.Song.popularity.desc()).all()
    elif (weather == 'windy'):
        songs = db.query(models.Song).filter(models.Song.beats_per_minute >= 111, models.Song.beats_per_minute <= 137).order_by(models.Song.popularity.desc()).all()
    elif (weather == 'rainy'):
        songs = db.query(models.Song).filter(models.Song.beats_per_minute >= 138, models.Song.beats_per_minute <= 164).order_by(models.Song.popularity.desc()).all()
    elif (weather == 'sunny'):
        songs = db.query(models.Song).filter(models.Song.beats_per_minute >= 165).order_by(models.Song.popularity.desc()).all()
    else:
        songs = 'Failed getting songs recommendation. Input must be sunny/windy/cloudy/rainy.'
    return songs