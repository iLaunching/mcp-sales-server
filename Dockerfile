FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY main.py .

# Expose port (Railway will set $PORT dynamically)
EXPOSE 8080

# Run server - Railway uses $PORT environment variable
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}
