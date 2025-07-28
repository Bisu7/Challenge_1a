# Use Python 3.9 slim image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the processing script
COPY process_pdfs.py .

# Create input and output directories
RUN mkdir -p /app/input /app/output

# Set the default command
CMD ["python", "process_pdfs.py"]