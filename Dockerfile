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
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Ensure PyNaCl dependencies are installed
RUN pip install --no-cache-dir --force-reinstall pynacl numpy pydub

# Copy project files
COPY . .

# Create and activate a virtual environment
RUN python3 -m venv /app/venv

# Use the virtual environment for pip
RUN /app/venv/bin/pip install --upgrade pip
RUN /app/venv/bin/pip install --no-cache-dir --force-reinstall -r requirements.txt

# Set the default command to use the virtual environment
CMD ["/app/venv/bin/python", "main.py"]
