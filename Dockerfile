# ----------- Node Stage -----------
FROM node:18 AS node-builder

WORKDIR /app

# Prevent husky Git hook setup
ENV HUSKY=0

# Copy and install only package files
COPY package*.json ./
RUN npm install --legacy-peer-deps --force

# Copy all project files
COPY . .

# ----------- Python Final Stage -----------
FROM python:3.10-slim

WORKDIR /app

# Set environment variables to noninteractive to avoid prompts
ENV DEBIAN_FRONTEND=noninteractive

# Update system and install required tools
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        git \
        curl \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Create Python virtual environment
RUN python -m venv /app/venv

# Upgrade pip, setuptools, and wheel
RUN /app/venv/bin/pip install --upgrade pip setuptools wheel

# Copy only requirements and install them
COPY requirements.txt .
RUN /app/venv/bin/pip install --no-cache-dir -r requirements.txt

# Copy all app code from node-builder
COPY --from=node-builder /app /app

# Start the Python app
CMD ["/app/venv/bin/python", "main.py"]
