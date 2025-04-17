#!/bin/bash
# This script pulls the necessary models for the TicketAssist application

# Wait for Ollama service to be ready
echo "Waiting for Ollama service to be ready..."
until $(curl --output /dev/null --silent --head --fail http://ollama:11434); do
    printf '.'
    sleep 5
done

echo "Ollama service is ready. Pulling models..."

# Pull the Llama3 model
echo "Pulling Llama3 (8B) model..."
curl -X POST http://ollama:11434/api/pull -d '{"name":"llama3.1:8b"}'

echo "Model setup complete!"