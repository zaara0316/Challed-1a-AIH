# process_pdfs.py

import os
import json
from heading_extractor import extract_headings_with_fallback

INPUT_DIR = "./input"
OUTPUT_DIR = "./output"

def process_pdf_file(pdf_path):
    # Extract everything (including a Title entry)
    flat = extract_headings_with_fallback(pdf_path)

    # Pull out the title
    title = None
    outline = []
    for entry in flat:
        if entry.get("level") == "Title" and title is None:
            title = entry["text"]
        else:
            # Only include H1–H3 entries in the outline
            outline.append({
                "level": entry["level"],
                "text":  entry["text"],
                "page":  entry["page"]
            })

    # Fallback if no title detected
    if title is None and outline:
        title = outline[0]["text"]

    return {"title": title or "", "outline": outline}


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for fname in os.listdir(INPUT_DIR):
        if not fname.lower().endswith(".pdf"):
            continue

        pdf_path    = os.path.join(INPUT_DIR, fname)
        result      = process_pdf_file(pdf_path)
        out_fname   = os.path.splitext(fname)[0] + "_outline.json"
        out_path    = os.path.join(OUTPUT_DIR, out_fname)

        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
