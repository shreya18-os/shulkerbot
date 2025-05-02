# ----------- Node Stage -----------
FROM node:18 AS node-builder

WORKDIR /app

# Prevent husky errors
ENV HUSKY=0

# Copy only package files first
COPY package*.json ./

# Install Node.js dependencies
RUN npm install --legacy-peer-deps --force

# Copy the rest of the Node.js app
COPY . .

# ----------- Python Final Stage -----------
FROM python:3.10-slim

WORKDIR /app

# Install git
RUN apt-get update && \
    apt-get install -y git && \
    rm -rf /var/lib/apt/lists/*

# Setup venv
RUN python -m venv /app/venv

# Upgrade pip and tools
RUN /app/venv/bin/pip install --upgrade pip setuptools wheel

# Copy Python dependencies
COPY requirements.txt .

# Install Python dependencies
RUN /app/venv/bin/pip install --no-cache-dir -r requirements.txt

# Copy everything from Node.js stage
COPY --from=node-builder /app /app

# Set entry point
CMD ["/app/venv/bin/python", "main.py"]
