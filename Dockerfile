FROM python:3.10-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    poppler-utils tesseract-ocr \
    tesseract-ocr-jpn tesseract-ocr-hin tesseract-ocr-eng \
    libgl1 libglib2.0-0 && \
    apt-get clean

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "process_pdfs.py"]
