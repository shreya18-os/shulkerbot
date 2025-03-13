# Use Python 3.10
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install Git and other dependencies
RUN apt-get update && \
    apt-get install -y git && \
    rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /app/venv

# Upgrade pip and essential tools
RUN /app/venv/bin/pip install --upgrade pip setuptools wheel

# Copy requirements.txt
COPY requirements.txt .

# **Pass GitHub token securely**
ARG GH_TOKEN
RUN git config --global url."https://${GH_TOKEN}@github.com/".insteadOf "https://github.com/"

# Install dependencies from requirements.txt
RUN /app/venv/bin/pip install --no-cache-dir -r requirements.txt

# Copy your bot code
COPY . .

# Run the bot
CMD ["/app/venv/bin/python", "main.py"]
