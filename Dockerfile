# Use a lightweight Python image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    ffmpeg \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . .

# Create virtual environment
RUN python3 -m venv /app/venv

# Install dependencies from requirements.txt
RUN /app/venv/bin/pip install --upgrade pip
RUN /app/venv/bin/pip install --no-cache-dir --progress=off -r requirements.txt


# Set the default command to run the bot
CMD ["/app/venv/bin/python", "main.py"]
