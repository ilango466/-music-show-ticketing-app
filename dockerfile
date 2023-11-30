FROM python:3.8-slim

WORKDIR /app

EXPOSE 80

COPY . .

ls -l

RUN pip install --upgrade pip && \
        pip install -r requirement.txt

ENTRYPOINT python music_app.py
