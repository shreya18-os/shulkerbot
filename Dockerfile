FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install git
RUN apt-get update && \
    apt-get install -y git && \
    rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /app/venv

# Upgrade pip, setuptools and wheel
RUN /app/venv/bin/pip install --upgrade pip setuptools wheel

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN /app/venv/bin/pip install --no-cache-dir -r requirements.txt

# Copy the entire bot code
COPY . .

# Run the bot
CMD ["/app/venv/bin/python", "bot.py"]
