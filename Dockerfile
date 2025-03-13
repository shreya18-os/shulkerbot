# Use the official Python image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install Git
RUN apt-get update && \
    apt-get install -y git && \
    rm -rf /var/lib/apt/lists/*

# Create a virtual environment
RUN python -m venv /app/venv

# Upgrade pip, setuptools, and wheel
RUN /app/venv/bin/pip install --upgrade pip setuptools wheel

# Copy requirements.txt into the container
COPY requirements.txt .

# Install dependencies
RUN /app/venv/bin/pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Set the entry point for your application (adjust as needed)
CMD ["/app/venv/bin/python", "your_main_script.py"]
