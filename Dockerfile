# Use a minimal base image with Python
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the script
CMD ["python", "process_pdfs.py"]
