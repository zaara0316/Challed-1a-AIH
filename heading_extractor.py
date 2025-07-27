import fitz
from ocr_utils import ocr_page_as_text
from language_utils import detect_script
import unicodedata

def is_garbage(text):
    return len(text.strip()) < 2 or all(not c.isalnum() for c in text.strip())

def extract_outline(doc, filename):
    outline = []
    font_counter = {}
    all_spans = []
    title = ""
    pages_with_text = set()

    for page_num, page in enumerate(doc, start=0):
        spans = []
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    text = span["text"].strip()
                    size = round(span["size"], 1)
                    if not text or is_garbage(text):
                        continue
                    font_counter[size] = font_counter.get(size, 0) + 1
                    spans.append({
                        "text": text,
                        "size": size,
                        "page": page_num
                    })
                    pages_with_text.add(page_num)
        all_spans.extend(spans)

    top_sizes = sorted(font_counter, reverse=True)
    size_map = {}
    if len(top_sizes) > 0: size_map[top_sizes[0]] = "H1"
    if len(top_sizes) > 1: size_map[top_sizes[1]] = "H2"
    if len(top_sizes) > 2: size_map[top_sizes[2]] = "H3"

    for span in all_spans:
        size = span["size"]
        if size in size_map:
            outline.append({
                "level": size_map[size],
                "text": span["text"],
                "page": span["page"],
                "script": detect_script(span["text"])
            })

    # OCR fallback for pages with no extractable text
    for page_num in range(1, len(doc) + 1):
        if page_num not in pages_with_text:
            ocr_text = ocr_page_as_text(doc, page_num - 1)
            if ocr_text.strip():
                outline.append({
                    "level": "H1",
                    "text": ocr_text[:50],
                    "page": page_num,
                    "script": detect_script(ocr_text)
                })

    return {
        "title": title if title else filename.replace(".pdf", ""),
        "outline": sorted(outline, key=lambda x: x["page"])
    }
