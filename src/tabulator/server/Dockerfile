# Dockerfile
FROM python:3.6.9

RUN pip install Flask gunicorn
RUN pip install pyrebase
RUN apt-get update ##[edited]
RUN apt-get install ffmpeg libsm6 libxext6  -y
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY src/ app/ 
WORKDIR /app
ADD . /scripts

ENV PORT 8080

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app