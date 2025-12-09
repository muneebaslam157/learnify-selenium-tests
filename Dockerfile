# Use official Python runtime as base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies (minimal - webdriver-manager will handle Chrome)
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    ca-certificates \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy test file
COPY test_learnify_automation.py .

# Set environment
ENV APP_URL=http://localhost:5173

# Run tests
CMD ["python", "-m", "unittest", "test_learnify_automation", "-v"]
