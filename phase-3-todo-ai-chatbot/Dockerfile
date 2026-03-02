FROM python:3.10

WORKDIR /app

# Copy requirements first
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Set Python path
ENV PYTHONPATH=/app/backend/src

# Run using run.py (which has proper path setup)
# REBUILD TRIGGER: 2026-02-25 18:00
CMD ["python", "run.py"]
