# Base image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install required packages
RUN apt-get update && apt-get install -y \
    git \
    ffmpeg \
    gcc \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /app/venv

# Activate virtual environment and upgrade pip
RUN /app/venv/bin/pip install --upgrade pip setuptools wheel

# Copy requirements file
COPY requirements.txt .

# Install dependencies with GitHub token as an argument
ARG GH_TOKEN
RUN git config --global url."https://${GH_TOKEN}@github.com/".insteadOf "https://github.com/"
RUN /app/venv/bin/pip install --no-cache-dir -r requirements.txt


# Copy all the code to the app
COPY . .

# Set the entry point for running the bot
CMD ["/app/venv/bin/python", "bot.py"]
