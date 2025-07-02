#!/bin/bash

# Quick Start Azure Magentic-UI Script
echo "🚀 Quick starting Magentic-UI with Azure OpenAI..."

# Activate virtual environment
if [ -d ".venv" ]; then
    source .venv/bin/activate
    echo "✅ Virtual environment activated"
else
    echo "❌ Virtual environment not found. Please run the full setup first."
    exit 1
fi

# Run Magentic-UI with Azure configuration
echo "🌟 Starting Magentic-UI with Azure configuration..."
magentic-ui --config azure_config.yaml --port 8081
