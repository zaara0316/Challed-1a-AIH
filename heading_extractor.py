import fitz
from utils import is_heading, merge_multiline_headings
from ocr_fallback import extract_text_with_tesseract
from collections import Counter

def extract_headings_with_fallback(pdf_path):
    doc = fitz.open(pdf_path)
    headings = []
    all_sizes = []
    candidate_lines = []
    seen_texts = set()

    possible_titles = []
    page0_text_blocks = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        blocks = page.get_text("dict")["blocks"]
        text_blocks = []

        for block in blocks:
            for line in block.get("lines", []):
                line_text = " ".join([span["text"] for span in line["spans"]]).strip()
                if not line_text:
                    continue
                font_size = max([span["size"] for span in line["spans"]])
                text_blocks.append((line_text, font_size))

        if not text_blocks:
            ocr_lines = extract_text_with_tesseract(pdf_path, page_num)
            text_blocks = [(line.strip(), 12) for line in ocr_lines]

        merged = merge_multiline_headings(text_blocks)
        all_sizes.extend([size for _, size in merged if size is not None])

        if page_num <= 1:
            page0_text_blocks.extend(merged)

        for text, size in merged:
            if is_heading(text):
                candidate_lines.append((text, size, page_num))

    # Map font size to levels
    size_counts = Counter(all_sizes)
    top_sizes = sorted(size_counts.items(), key=lambda x: (-x[1], -x[0]))
    level_map = {}
    for i, (size, _) in enumerate(top_sizes[:3]):
        level_map[size] = f"H{i+1}"

    for text, size, page in candidate_lines:
        if text in seen_texts or size not in level_map:
            continue
        seen_texts.add(text)
        headings.append({
            "level": level_map[size],
            "text": text,
            "page": page
        })

    # Find best title: largest heading-like line on page 0 or 1
    sorted_by_size = sorted(page0_text_blocks, key=lambda x: -x[1])
    for text, size in sorted_by_size:
        if is_heading(text) and len(text) > 20 and "RFP:" not in text:
            headings.insert(0, {
                "level": "Title",
                "text": text,
                "page": 0
            })
            break

    return headings
