# Use a lightweight Python image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install required system dependencies
RUN apt-get update && apt-get install -y \
    software-properties-common \
    build-essential \
    wget \
    curl \
    python3-venv \
    sqlite3 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . .

# Create and activate virtual environment
RUN python3 -m venv /app/venv

# Install required Python modules
RUN /app/venv/bin/pip install --upgrade pip setuptools wheel

# Install all dependencies
RUN /app/venv/bin/pip install --no-cache-dir "discord.py[voice]" discord-ext-voice pydub numpy requests


# Set the default command to run the bot
CMD ["/app/venv/bin/python", "main.py"]
