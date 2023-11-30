FROM python:3.8-slim

WORKDIR /app

EXPOSE 80

COPY . .

RUN pip install --upgrade pip && \
        pip install -r requirement.txt

ENTRYPOINT python music_app.py