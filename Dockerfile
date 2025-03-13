# Use the official Python image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install git to clone discord-ext-voice
RUN apt-get update && apt-get install -y git ffmpeg

# Create virtual environment
RUN python -m venv /app/venv

# Activate virtual environment
ENV PATH="/app/venv/bin:$PATH"

# Upgrade pip
RUN pip install --upgrade pip

# Copy requirements.txt
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all the bot files
COPY . .

# Run the bot
CMD ["python", "main.py"]
