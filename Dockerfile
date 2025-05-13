# ----------- Node Stage -----------
FROM node:18 AS node-builder

WORKDIR /app
ENV HUSKY=0

COPY package*.json ./
RUN npm install --legacy-peer-deps --force

COPY . .

# ----------- Python Final Stage -----------
FROM python:3.10-slim

WORKDIR /app
ENV DEBIAN_FRONTEND=noninteractive

# Split the apt-get into two separate RUN steps to reduce memory spike
RUN apt-get update
RUN apt-get install -y --no-install-recommends git curl ca-certificates && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN python -m venv /app/venv

# Upgrade pip and tools (in a separate layer to isolate memory usage)
RUN /app/venv/bin/pip install --upgrade pip setuptools wheel

COPY requirements.txt .
RUN /app/venv/bin/pip install --no-cache-dir -r requirements.txt

COPY --from=node-builder /app /app

CMD ["/app/venv/bin/python", "main.py"]
