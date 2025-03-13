FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install Git
RUN apt-get update && \
    apt-get install -y git && \
    rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /app/venv

# Upgrade pip, setuptools, and wheel
RUN /app/venv/bin/pip install --upgrade pip setuptools wheel

# Set the GitHub token argument
ARG GH_TOKEN

# Configure Git to use the token for GitHub authentication
RUN git config --global url."https://${GH_TOKEN}@github.com/".insteadOf "https://github.com/"

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN /app/venv/bin/pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files
COPY . .

# Set the entry point
CMD ["/app/venv/bin/python", "bot.py"]
