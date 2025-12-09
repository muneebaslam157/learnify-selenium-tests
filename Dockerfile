FROM python:3.11-slim

WORKDIR /app

# Install system dependencies and Chromium
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    ca-certificates \
    gnupg \
    lsb-release \
    fonts-liberation \
    libnss3 \
    libxss1 \
    xdg-utils \
    chromium \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir selenium>=4.15.0 webdriver-manager>=4.0.0

# Copy test file
COPY test_learnify_automation.py .

# Set environment variables
ENV APP_URL=http://localhost:5173
ENV CHROME_BIN=/usr/bin/chromium

# Run tests
CMD ["python", "-m", "unittest", "test_learnify_automation", "-v"]
