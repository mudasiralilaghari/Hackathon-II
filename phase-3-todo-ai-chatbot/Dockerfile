# Dockerfile for Hugging Face Spaces Deployment
# Phase-3: Todo AI Chatbot Backend

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Expose the port Hugging Face expects
EXPOSE 7860

# Set environment variables
ENV HOST=0.0.0.0
ENV PORT=7860

# Run the backend
CMD ["python", "run.py", "--host", "0.0.0.0", "--port", "7860"]
