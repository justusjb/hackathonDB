FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy shared package
COPY shared/ /app/shared/

# Install shared package
RUN pip install --no-cache-dir -e /app/shared/

# Copy backend requirements and install dependencies
COPY backend/requirements.txt /app/backend/
WORKDIR /app/backend
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ /app/backend/

# Default environment variables
ENV PORT=8000

# Expose the port
EXPOSE $PORT

# Start the application
CMD uvicorn main:app --host 0.0.0.0 --port $PORT