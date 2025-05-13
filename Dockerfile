# ----------- Python Only Stage -----------
FROM python:3.10-slim

WORKDIR /app
ENV DEBIAN_FRONTEND=noninteractive

# Install tools
RUN apt-get update && \
    apt-get install -y --no-install-recommends git curl ca-certificates && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Python environment setup
RUN python -m venv /app/venv
RUN /app/venv/bin/pip install --upgrade pip setuptools wheel

# Copy requirements and install
COPY requirements.txt .
RUN /app/venv/bin/pip install --no-cache-dir -r requirements.txt

# Copy rest of the app
COPY . .

# Run your Python app
CMD ["/app/venv/bin/python", "main.py"]
