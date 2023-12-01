FROM python:3.8-slim

WORKDIR /app

EXPOSE 5000

COPY . .

RUN pip install --upgrade pip && \
        pip install -r requirement.txt

CMD ["python", "music_app.py"]
