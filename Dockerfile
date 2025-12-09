# Use official Python runtime with Chrome support
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies and Chrome
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
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Add Google Chrome repository and install Chrome
RUN curl https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - 2>/dev/null || true && \
    sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' && \
    apt-get update && \
    apt-get install -y google-chrome-stable --no-install-recommends && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy and install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy test file
COPY test_learnify_automation.py .

# Set environment
ENV APP_URL=http://localhost:5173

# Run tests
CMD ["python", "-m", "unittest", "test_learnify_automation", "-v"]
