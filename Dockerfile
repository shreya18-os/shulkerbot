# Use Python Slim image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y \
    git \
    ffmpeg \
    gcc \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /app/venv

# Upgrade pip, setuptools, wheel
RUN /app/venv/bin/pip install --upgrade pip setuptools wheel

# Copy requirements.txt
COPY requirements.txt .

# Install dependencies (including discord-ext-voice)
RUN /app/venv/bin/pip install --no-cache-dir -r requirements.txt \
    --extra-index-url https://kkrypt0nn:$GH_TOKEN@github.com/kkrypt0nn/discord-ext-voice.git

# Copy all bot files
COPY . .

# Run the bot
CMD ["/app/venv/bin/python", "bot.py"]
