# Genereate dockerfile for fastapi application with python 3.11
FROM python:3.11-slim-bullseye

WORKDIR /app

COPY requirements.txt .
RUN ---mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt

COPY ./app ./app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
