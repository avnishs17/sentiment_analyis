# Use NVIDIA CUDA base image
FROM nvidia/cuda:11.8.0-base-ubuntu22.04

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3 \
    python3-pip \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Ensure the templates directory exists
COPY templates/index.html /app/templates/

# Set the transformers cache directory
ENV TRANSFORMERS_CACHE=/app/model/model_cache

# Run tests
RUN python3 -m unittest discover tests

# Expose the port the app runs on
EXPOSE 8000

# Create a non-root user and switch to it
RUN useradd -m myuser
USER myuser

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]