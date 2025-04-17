#!/bin/bash
# Startup script for TicketAssist services

# Make sure we're in the right directory
cd "$(dirname "$0")"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
  echo "Error: Docker does not appear to be running. Please start Docker and try again."
  exit 1
fi

# Stop any existing containers to ensure a clean start
echo "Stopping any existing containers..."
docker-compose down

# Start services
echo "Starting services..."
docker-compose up -d

# Wait for Ollama to be ready
echo "Waiting for Ollama service to initialize..."
ATTEMPTS=0
MAX_ATTEMPTS=30

until $(curl --output /dev/null --silent --fail http://localhost:11434/api/version) || [ $ATTEMPTS -eq $MAX_ATTEMPTS ]; do
  ATTEMPTS=$((ATTEMPTS+1))
  echo "Attempt $ATTEMPTS/$MAX_ATTEMPTS: Waiting for Ollama to be ready..."
  sleep 10
done

if [ $ATTEMPTS -eq $MAX_ATTEMPTS ]; then
  echo "Ollama service failed to start properly after 5 minutes."
  echo "Please check the logs with: docker logs ollama"
  exit 1
fi

# Check if the model is already pulled
if ! docker exec ollama ollama list | grep -q "llama3.1:8b"; then
  echo "Pulling the Llama3 model (this may take some time)..."
  docker exec ollama ollama pull llama3.1:8b
else
  echo "Llama3 model already available."
fi

echo "Initialization complete! TicketAssist is running at http://localhost:8501"