#!/bin/bash
# Setup script for Docker secrets

# Create the secrets directory if it doesn't exist
mkdir -p ./secrets

# Function to create a secret file
create_secret() {
  local secret_name=$1
  local prompt_text=$2
  local default_value=$3

  if [ -f "./secrets/${secret_name}.txt" ]; then
    echo "Secret ${secret_name} already exists."
  else
    echo -n "${prompt_text} (default: ${default_value}): "
    read secret_value
    if [ -z "$secret_value" ]; then
      secret_value=$default_value
    fi
    echo -n "$secret_value" > "./secrets/${secret_name}.txt"
    echo "Created secret ${secret_name}."
  fi
}

# Create secrets
create_secret "replicate_api_token" "Enter your Replicate API Token" "r8_your_token_here"
create_secret "streamlit_auth_user" "Enter admin username" "admin"
create_secret "streamlit_auth_password" "Enter admin password" "admin"

echo ""
echo "Secrets created successfully. Now you can use them with docker-compose.prod.yml:"
echo "docker-compose -f docker-compose.prod.yml up -d"