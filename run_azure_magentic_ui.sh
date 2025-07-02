#!/bin/bash

# Azure Magentic-UI Setup and Run Script
echo "Setting up Magentic-UI with Azure OpenAI..."

# Set Azure environment variables
export AZURE_API_KEY="9FNrC8BdOJqArMJRfoC3lk6tpjkQZ3dLDfccEGR4wLnvJTf1mIO6JQQJ99BCACHYHv6XJ3w3AAAAACOGyxtr"
export AZURE_ENDPOINT="https://dctassistresou5125686331.cognitiveservices.azure.com"
export AZURE_API_VERSION="2024-02-15-preview"
export AZURE_DEPLOYMENT_NAME="gpt-4o"

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Install Magentic-UI with Azure support
echo "Installing Magentic-UI with Azure dependencies..."
pip install --upgrade pip
pip install magentic-ui[azure] --upgrade

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker Desktop first."
    exit 1
fi

echo "🚀 Starting Magentic-UI with Azure OpenAI configuration..."
echo "📊 Using Azure endpoint: $AZURE_ENDPOINT"
echo "🔧 Using deployment: $AZURE_DEPLOYMENT_NAME"

# Run Magentic-UI with Azure configuration
magentic-ui --config azure_config.yaml --port 8081

echo "✅ Magentic-UI should now be running at http://localhost:8081"