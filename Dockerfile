# ----------- Python Only Stage -----------
FROM python:3.10-slim

# Set working directory
WORKDIR /app
ENV DEBIAN_FRONTEND=noninteractive

# Install essential tools and venv dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    python3-venv \
    python3-dev \
    gcc \
    git \
    curl \
    ca-certificates && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python3 -m venv /app/venv

# Upgrade pip and install requirements
COPY requirements.txt .
RUN /app/venv/bin/pip install --upgrade pip setuptools wheel && \
    /app/venv/bin/pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Run the application
CMD ["/app/venv/bin/python", "main.py"]
