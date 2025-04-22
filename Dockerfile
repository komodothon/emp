# Dockerfile

# Use Python 3.11 slim version for smaller image size
FROM python:3.11-slim

# Set environment variables
ENV FLASK_ENV=development
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory inside the container
WORKDIR /code
COPY . .

# Install build tools (needed for some pip packages)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Explicitly install flask-migrate if not already in requirements.txt
RUN pip install flask-migrate

# Copy all app files including seed, templates, etc.
COPY . .

# Make entrypoint script executable
RUN chmod +x /code/entrypoint.sh

# Expose port for the app
EXPOSE 8000

# Run the entrypoint script (relative to WORKDIR /app)
ENTRYPOINT ["./entrypoint.sh"]
