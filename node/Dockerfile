FROM python:3.11-slim

WORKDIR /app

COPY node /app
COPY shared /app/shared

RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /app/data

EXPOSE 5000

CMD ["sh", "-c", "uvicorn node:app --host 0.0.0.0 --port ${PORT}"]