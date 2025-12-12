FROM python:3.9-slim

WORKDIR /app

# Install system dependencies if any (none for now based on requirements)

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire mcp directory content into /app
# Since we are building from mcp directory context or parent, we need to be careful.
# If build context is ., then COPY . . works.
COPY . .

# Expose the port
EXPOSE 9000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9000"]
