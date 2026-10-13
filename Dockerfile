FROM python:3.11-slim

# Install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements
COPY requirements.txt .
COPY web-ui/requirements.txt ./web-ui/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r web-ui/requirements.txt
RUN pip install --no-cache-dir gunicorn

# Copy application code
COPY . .

WORKDIR /app/web-ui

# Expose port
EXPOSE 8080

# Run the application
CMD gunicorn -w 2 -b 0.0.0.0:$PORT app:app --timeout 600
