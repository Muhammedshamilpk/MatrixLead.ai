FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies (optional but recommended)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire agents directory
COPY . .

# Expose port for agents service
EXPOSE 8010

# Start the agent runner API
CMD ["uvicorn", "agent_runner:app", "--host", "0.0.0.0", "--port", "8010"]
