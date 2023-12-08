FROM python:3.8-slim

WORKDIR /app

EXPOSE 5000

COPY . .

RUN pip install --upgrade pip && \
        pip install -r requirement.txt

CMD gunicorn --bind 0.0.0.0:5000 music_app:app
