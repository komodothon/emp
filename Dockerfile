# Dockerfile

# Use Python 3.11 slim version for smaller image size
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Install build tools and optional system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .

# Copy and make entrypoint executable
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000

# Start from entrypoint
ENTRYPOINT ["/entrypoint.sh"]
