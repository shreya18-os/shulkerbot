# ----------- Python Only Stage -----------
FROM python:3.10-slim

# Set working directory
WORKDIR /app
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies needed for building Python packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    python3-venv \
    python3-dev \
    gcc \
    libffi-dev \
    libssl-dev \
    curl \
    git \
    ca-certificates && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker layer caching
COPY requirements.txt .

# Create and activate virtual environment, install dependencies
RUN python3 -m venv /app/venv && \
    /app/venv/bin/pip install --upgrade pip setuptools wheel && \
    /app/venv/bin/pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Set environment path so CMD can find Python packages
ENV PATH="/app/venv/bin:$PATH"

# Start the application
CMD ["python", "main.py"]
