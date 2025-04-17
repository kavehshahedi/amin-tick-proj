# Docker Setup for TicketAssist

This guide provides instructions for setting up and running TicketAssist using Docker and Docker Compose.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- NVIDIA Docker (optional, for GPU acceleration with Ollama)

## Files Overview

1. `Dockerfile` - Defines the TicketAssist application container
2. `docker-compose.yml` - Orchestrates TicketAssist and Ollama services with environment variables
3. `docker-compose.prod.yml` - Production deployment with Docker Secrets
4. `.env.template` - Template for environment variables (copy to `.env`)
5. `.dockerignore` - Specifies files to exclude from the Docker build
6. `ollama-setup.sh` - Script to initialize Ollama and pull required models
7. `setup-secrets.sh` - Script to set up Docker secrets for production deployment

## Quick Start (Development)

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ticketassist.git
   cd ticketassist
   ```

2. Create environment file from template:
   ```bash
   cp .env.template .env
   ```

3. Edit the `.env` file to set your API keys and other configurations:
   ```bash
   # Replace with your actual keys and settings
   REPLICATE_API_TOKEN=your_actual_token
   STREAMLIT_AUTH_USER=your_username
   STREAMLIT_AUTH_PASSWORD=your_password
   ```

4. Make the Ollama setup script executable:
   ```bash
   chmod +x ollama-setup.sh
   ```

5. Start the services:
   ```bash
   docker-compose up -d
   ```

6. Initialize the Ollama models (after the Ollama service is running):
   ```bash
   docker exec -it ollama /bin/bash -c "cd /app && ./ollama-setup.sh"
   ```

7. Access TicketAssist at [http://localhost:8501](http://localhost:8501)

## Production Deployment

For production environments, use Docker Secrets for enhanced security:

1. Make the setup script executable:
   ```bash
   chmod +x setup-secrets.sh
   ```

2. Run the script to create your secrets:
   ```bash
   ./setup-secrets.sh
   ```

3. Start the application with the production compose file:
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

## Configuration

### API Keys and Credentials

#### Development Mode (.env file)

For development, TicketAssist uses environment variables defined in the `.env` file:

1. Copy the template:
   ```bash
   cp .env.template .env
   ```

2. Edit the `.env` file to configure:
   - API tokens (Replicate, etc.)
   - Authentication credentials
   - LLM parameters
   - App settings

All these environment variables are automatically loaded by Docker Compose.

#### Production Mode (Docker Secrets)

For production, use Docker Secrets for enhanced security:

1. Make the setup script executable:
   ```bash
   chmod +x setup-secrets.sh
   ```

2. Run the script to create your secrets:
   ```bash
   ./setup-secrets.sh
   ```

3. Start the application with the production compose file:
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

This approach is more secure as secrets are mounted as files rather than environment variables.

### GPU Support

The `docker-compose.yml` file includes NVIDIA GPU configurations for Ollama. If you don't have a GPU or NVIDIA Docker installed, modify the `docker-compose.yml` file to remove the GPU-specific configurations:

```yaml
# Remove or comment out these lines
deploy:
  resources:
    reservations:
      devices:
        - driver: nvidia
          count: all
          capabilities: [gpu]
```

### Persistent Data

Data persistence is configured through Docker volumes:

- `./data:/app/data` - Mounts the local `data` directory for persistent application data
- `ollama-data:/root/.ollama` - Named volume for Ollama models and configurations

### Environment Variables Reference

Key environment variables that can be configured:

```
# API Tokens
REPLICATE_API_TOKEN=r8_your_replicate_token_here

# Authentication Credentials
STREAMLIT_AUTH_USER=admin
STREAMLIT_AUTH_PASSWORD=admin

# LLM Parameters
LLM_MODEL=llama3.1:8b
LLM_TEMPERATURE=0.1
LLM_MAX_TOKENS=512
LLM_TOP_P=0.9

# App Settings
APP_TITLE=TicketAssist
DEBUG_MODE=false

# Service Configuration
OLLAMA_API_HOST=http://ollama:11434
```

## Troubleshooting

### Container Logs

View container logs to diagnose issues:

```bash
# TicketAssist logs
docker logs ticketassist

# Ollama logs
docker logs ollama
```

### Ollama Model Issues

If you encounter issues with Ollama models:

1. Check if the model is properly pulled:
   ```bash
   docker exec -it ollama ollama list
   ```

2. Manually pull the model if needed:
   ```bash
   docker exec -it ollama ollama pull llama3.1:8b
   ```

### Container Health Checks

The `ticketassist` container includes health checks. Check container health:

```bash
docker inspect --format='{{.State.Health.Status}}' ticketassist
```

## Maintenance

### Updating the Application

To update the application with new code:

```bash
# Pull the latest code changes
git pull

# Rebuild and restart the containers
docker-compose up -d --build
```

### Stopping the Services

To stop the services:

```bash
docker-compose down
```

To stop and remove volumes (warning: this will delete persistent data):

```bash
docker-compose down -v
```

## Production Considerations

For production deployments, consider:

1. Using a production-ready web server (like Nginx) as a reverse proxy
2. Setting up proper authentication
3. Configuring HTTPS
4. Implementing container orchestration (Kubernetes)
5. Setting up monitoring and alerting