FROM python:3.13-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    g++ \
    git \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
ADD ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ADD . .

EXPOSE 80

ENTRYPOINT ./entrypoint.sh