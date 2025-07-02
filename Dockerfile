# Multi-stage build for Magentic-UI
FROM node:18-alpine AS frontend-builder

# Set working directory for frontend
WORKDIR /app/frontend

# Copy package files
COPY frontend/package.json frontend/package-lock.json* ./

# Install dependencies
RUN npm ci

# Copy frontend source code
COPY frontend/ ./

# Build the frontend
RUN npm run build

# Python backend stage
FROM python:3.11-slim AS backend

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    wget \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Install Docker (required by the application)
RUN curl -fsSL https://get.docker.com -o get-docker.sh && \
    sh get-docker.sh && \
    rm get-docker.sh

# Install uv for faster Python package management
RUN pip install uv

# Set working directory
WORKDIR /app

# Copy Python dependencies
COPY pyproject.toml uv.lock ./

# Install Python dependencies
RUN uv sync --frozen

# Copy source code
COPY src/ ./src/
COPY samples/ ./samples/
COPY tests/ ./tests/
COPY *.py ./
COPY *.yaml ./
COPY *.md ./
COPY *.ini ./
COPY *.sh ./

# Copy built frontend from previous stage
COPY --from=frontend-builder /app/frontend/public ./src/magentic_ui/backend/web/ui/

# Install the package
RUN uv pip install -e .

# Install playwright browsers
RUN playwright install

# Expose port
EXPOSE 8081

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8081 || exit 1

# Create entrypoint script
RUN echo '#!/bin/bash\n\
# Start Docker daemon in background if needed\n\
if ! pgrep dockerd > /dev/null; then\n\
    dockerd &\n\
    sleep 5\n\
fi\n\
\n\
# Run the application\n\
exec magentic-ui --port 8081 "$@"\n\
' > /app/entrypoint.sh && chmod +x /app/entrypoint.sh

# Set entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]
