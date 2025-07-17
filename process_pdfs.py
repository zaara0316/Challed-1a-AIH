import os
from heading_extractor import extract_outline
import json
import fitz  # PyMuPDF

INPUT_DIR = "/app/input"
OUTPUT_DIR = "/app/output"

def process_all_pdfs():
    for filename in os.listdir(INPUT_DIR):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(INPUT_DIR, filename)
            doc = fitz.open(pdf_path)
            outline = extract_outline(doc)
            json_filename = filename.replace(".pdf", ".json")
            with open(os.path.join(OUTPUT_DIR, json_filename), "w") as f:
                json.dump(outline, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    process_all_pdfs()
