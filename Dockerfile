FROM debian:latest

# Update system and install required packages
RUN apt-get update && apt-get install -y \
    software-properties-common \
    build-essential \
    wget \
    curl \
    python3 \
    python3-pip \
    python3-venv \
    sqlite3 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy bot files into the container
COPY . .

# Install dependencies
RUN pip3 install -r requirements.txt

# Start the bot
CMD ["python3", "main.py"]
