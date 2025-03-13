# Use Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y git && \
    rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /app/venv

# Upgrade pip, setuptools, wheel
RUN /app/venv/bin/pip install --upgrade pip setuptools wheel

# Pass GitHub Token as argument
ARG GH_TOKEN

# Use GitHub Token to bypass authentication for private repos
RUN git config --global url."https://${GH_TOKEN}@github.com/".insteadOf "https://github.com/"

# Copy the requirements file
COPY requirements.txt .

# Install Python dependencies
RUN /app/venv/bin/pip install --no-cache-dir -r requirements.txt

# Copy the bot files
COPY . .

# Run the bot
CMD ["/app/venv/bin/python", "main.py"]
