
# Create Dockerfile
dockerfile = '''# Build stage
FROM node:18-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

# Production stage
FROM node:18-alpine

WORKDIR /app

RUN npm install -g http-server

COPY --from=builder /app/dist ./dist

EXPOSE 8000

CMD ["http-server", "dist", "-p", "8000", "--cors"]
'''

with open('greenfuel-frontend/Dockerfile', 'w') as f:
    f.write(dockerfile)

# Create docker-compose.yml
docker_compose = '''version: '3.8'

services:
  frontend:
    build: .
    ports:
      - "3000:3000"
    volumes:
      - ./src:/app/src
      - /app/node_modules
    environment:
      - REACT_APP_API_BASE_URL=http://localhost:5000
      - REACT_APP_USE_MOCK_PREDICTIONS=false
    command: npm start

  backend:
    image: python:3.9
    working_dir: /app
    ports:
      - "5000:5000"
    volumes:
      - ../greenfuel-ml-frontend:/app
    environment:
      - FLASK_APP=app.py
      - FLASK_ENV=production
    command: >
      bash -c "pip install -r requirements.txt &&
               python app.py"
    depends_on:
      - frontend
'''

with open('greenfuel-frontend/docker-compose.yml', 'w') as f:
    f.write(docker_compose)

print("✓ Created Dockerfile")
print("✓ Created docker-compose.yml")
