# Use official Python runtime as base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies including Chrome and ChromeDriver
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    ca-certificates \
    curl && \
    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] https://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && apt-get install -y google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

# Install ChromeDriver using webdriver-manager (simpler approach)
# Copy Python requirements first
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy test file
COPY test_learnify_automation.py .

# Set environment
ENV APP_URL=http://localhost:5173

# Run tests
CMD ["python", "-m", "unittest", "test_learnify_automation", "-v"]
