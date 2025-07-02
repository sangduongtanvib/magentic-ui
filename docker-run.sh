#!/bin/bash

# Build and run Magentic-UI with Docker

set -e

echo "🐳 Building Magentic-UI Docker image..."

# Build the Docker image
docker build -t magentic-ui:latest .

echo "✅ Docker image built successfully!"

echo "🚀 Starting Magentic-UI..."

# Run the container
docker run -d \
  --name magentic-ui \
  -p 8081:8081 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v magentic_data:/app/data \
  --privileged \
  -e OPENAI_API_KEY="${OPENAI_API_KEY}" \
  -e AZURE_OPENAI_API_KEY="${AZURE_OPENAI_API_KEY}" \
  -e AZURE_OPENAI_ENDPOINT="${AZURE_OPENAI_ENDPOINT}" \
  magentic-ui:latest

echo "✅ Magentic-UI is starting..."
echo "🌐 Access the application at: http://localhost:8081"
echo ""
echo "📋 Useful commands:"
echo "  View logs: docker logs -f magentic-ui"
echo "  Stop: docker stop magentic-ui"
echo "  Remove: docker rm magentic-ui"
echo "  Restart: docker restart magentic-ui"
