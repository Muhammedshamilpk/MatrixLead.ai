FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt
COPY main.py /app/main.py

RUN pip install --no-cache-dir -r requirements.txt


EXPOSE 9040

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9040"]
