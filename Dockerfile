# Use a minimal base image with Python
FROM --platform=linux/amd64 python:3.10-slim

# Set working directory
WORKDIR /app

# Copy files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Default command
CMD ["python", "process_pdfs.py"]
