FROM python:3.11-slim

# Prevent buffering (important for logging on Render)
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies required now and later (moviepy, ffmpeg, etc.)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (better caching)
COPY requirements.txt .

# Install python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire existing project structure EXACTLY as-is
COPY . .

# Render provides PORT env variable
ENV PORT=8000

# Start your existing FastAPI app
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT}"]
