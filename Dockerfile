FROM python:3.10.5
WORKDIR /tstAPI
COPY requirements.txt /tstAPI/requirements.txt
RUN pip3 install -r requirements.txt
COPY . /tstAPI
EXPOSE 8000

CMD ["uvicorn","songs_recs.main:app","--host=0.0.0.0","--reload"]