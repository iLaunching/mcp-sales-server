FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY main.py .
COPY start.sh .

# Make start script executable
RUN chmod +x start.sh

# Expose port (Railway will set $PORT dynamically)
EXPOSE 8080

# Run server using start script
CMD ["./start.sh"]
