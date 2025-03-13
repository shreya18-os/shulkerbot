# Use the official Python image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Create a virtual environment
RUN python -m venv /app/venv

# Install pip, setuptools, and wheel
RUN /app/venv/bin/pip install --upgrade pip setuptools wheel

# Copy the requirements file
COPY requirements.txt .

# Set GitHub token to access private repositories
ARG GIT_ACCESS_TOKEN

# Configure Git to use the token for authentication
RUN git config --global url."https://${GIT_ACCESS_TOKEN}@github.com/".insteadOf "https://github.com/"

# Install dependencies from requirements.txt
RUN /app/venv/bin/pip install --no-cache-dir -r requirements.txt

# Copy your bot files into the container
COPY . .

# Run the bot
CMD ["/app/venv/bin/python", "main.py"]
