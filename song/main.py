from fastapi import FastAPI
from . import schemas

app = FastAPI()



@app.post('/song')
def create(request: schemas.Song):
    return request