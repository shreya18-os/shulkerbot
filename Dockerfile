FROM python:3.10-slim

WORKDIR /app

# Install git
RUN apt-get update && \
    apt-get install -y git && \
    rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /app/venv

# Install pip, setuptools and wheel
RUN /app/venv/bin/pip install --upgrade pip setuptools wheel

# Authenticate with GitHub token
RUN git config --global url."https://x-access-token:${GH_TOKEN}@github.com/".insteadOf "https://github.com/"

# Copy requirements.txt
COPY requirements.txt .

# Install dependencies
RUN /app/venv/bin/pip install --no-cache-dir -r requirements.txt

# Copy all files
COPY . .

# Run bot
CMD ["/app/venv/bin/python", "main.py"]
