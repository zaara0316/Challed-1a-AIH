import os
import json
import fitz  # PyMuPDF
from heading_extractor import extract_outline
import json

INPUT_DIR = "input"
OUTPUT_DIR = "output"

def process_all_pdfs():
    for filename in os.listdir(INPUT_DIR):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(INPUT_DIR, filename)
            print(f"Processing: {filename}")
            doc = fitz.open(pdf_path)
            outline = extract_outline(doc, filename)
            output_path = os.path.join(OUTPUT_DIR, filename.replace(".pdf", ".json"))
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(outline, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    process_all_pdfs()
