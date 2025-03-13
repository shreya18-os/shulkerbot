FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y git && \
    rm -rf /var/lib/apt/lists/*

RUN python -m venv /app/venv

RUN /app/venv/bin/pip install --upgrade pip setuptools wheel

COPY requirements.txt .

RUN /app/venv/bin/pip install --no-cache-dir -r requirements.txt


COPY . .

CMD ["python", "main.py"]
