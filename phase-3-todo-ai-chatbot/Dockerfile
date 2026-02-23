FROM python:3.10

WORKDIR /app

# Copy requirements first
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend folder
COPY backend ./backend

# Set Python path to include backend/src
ENV PYTHONPATH=/app/backend/src

# Change to backend/src directory and run uvicorn
WORKDIR /app/backend/src

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
