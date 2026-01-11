FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies (for faiss, pdf, etc.)
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    curl \
    libgl1 \
    libgomp1 \
    libopenblas-dev \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*


    # Upgrade pip & wheel (important)
RUN pip install --upgrade pip setuptools wheel
    
# Copy dependency list
COPY requirements.txt .

# Install Python deps
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Run the API
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]