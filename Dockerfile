# ----------- Node Stage -----------
FROM node:18 AS node-builder

WORKDIR /app

# Prevent husky Git hook setup
ENV HUSKY=0

# Copy and install only package files
COPY package*.json ./
RUN npm install --legacy-peer-deps --force

# Copy source files after installing dependencies
COPY . .

# ----------- Python Final Stage -----------
FROM python:3.10-slim

WORKDIR /app

# Install git, curl, and certificates (needed for requests/disnake/etc)
RUN apt-get update && \
    apt-get install -y git curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /app/venv

# Upgrade pip and tools
RUN /app/venv/bin/pip install --upgrade pip setuptools wheel

# Copy requirements and install them
COPY requirements.txt ./
RUN /app/venv/bin/pip install --no-cache-dir -r requirements.txt

# Copy full project including node_modules from node-builder
COPY --from=node-builder /app /app

# Start the bot
CMD ["/app/venv/bin/python", "main.py"]
