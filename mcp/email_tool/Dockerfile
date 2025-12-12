FROM python:3.10-slim

WORKDIR /app

# Copy only THIS tool's files
COPY requirements.txt /app/requirements.txt
COPY main.py /app/main.py

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 9000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9000"]
