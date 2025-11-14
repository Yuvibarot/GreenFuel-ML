
# Create Dockerfile for containerization
dockerfile = '''FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app.py .
COPY scaler.pkl .
COPY labelencoder.pkl .
COPY GradientBoostingmodel.pkl .
COPY index.html templates/index.html

# Expose port
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--timeout", "120", "app:app"]
'''

with open('greenfuel-ml-frontend/Dockerfile', 'w') as f:
    f.write(dockerfile)

print("✓ Created Dockerfile")

# Create docker-compose.yml
docker_compose = '''version: '3.8'

services:
  greenfuel-api:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - PYTHONUNBUFFERED=1
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - greenfuel-api
    restart: unless-stopped
'''

with open('greenfuel-ml-frontend/docker-compose.yml', 'w') as f:
    f.write(docker_compose)

print("✓ Created docker-compose.yml")

# Create Procfile for Heroku
procfile = '''web: gunicorn --bind 0.0.0.0:$PORT app:app
'''

with open('greenfuel-ml-frontend/Procfile', 'w') as f:
    f.write(procfile)

print("✓ Created Procfile")
