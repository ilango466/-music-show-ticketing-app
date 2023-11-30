FROM python:3.8-slim

WORKDIR /app

EXPOSE 80

COPY ./requirement.txt /tmp

RUN pip install --upgrade pip && \
        pip install -r /tmp/requirement.txt && \
        rm -rf /tmp/requirement.txt

ENTRYPOINT python music_app.py
