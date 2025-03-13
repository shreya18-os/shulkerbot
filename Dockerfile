# Use the official Python image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Create a virtual environment
RUN python -m venv /app/venv

# Install pip, setuptools, and wheel
RUN /app/venv/bin/pip install --upgrade pip setuptools wheel

# Install Git (Railway doesn't have it by default)
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Set GitHub token to access private repositories
ENV GIT_TERMINAL_PROMPT=1
RUN git config --global url."https://${GH_TOKEN}@github.com/".insteadOf "https://github.com/"


# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN /app/venv/bin/pip install --no-cache-dir -r requirements.txt

# Copy the bot files
COPY . .

# Run the bot
CMD ["/app/venv/bin/python", "main.py"]

