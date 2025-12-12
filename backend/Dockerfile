FROM python:3.10-slim

WORKDIR /app

# Install Python dependencies first (faster builds)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy ONLY the app code (not .env)
COPY app ./app

# Enable auto-reload for development
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
