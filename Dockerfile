FROM python:3.10-slim

WORKDIR /app

# Set the GitHub Token
ARG GH_TOKEN

# Create virtual environment
RUN python -m venv /app/venv

# Install pip, setuptools, wheel
RUN /app/venv/bin/pip install --upgrade pip setuptools wheel

# GitHub Authentication Fix
RUN git config --global url."https://${GH_TOKEN}@github.com/".insteadOf "https://github.com/"

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN /app/venv/bin/pip install --no-cache-dir -r requirements.txt
