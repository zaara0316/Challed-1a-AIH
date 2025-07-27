from utils import clean_text, is_potential_heading, map_font_sizes_to_levels

def extract_outline(doc):
    outline = []
    title = ""

    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            for line in block.get("lines", []):
                for span in line["spans"]:
                    text = clean_text(span["text"])
                    if not text:
                        continue
                    size = round(span["size"], 1)
                    if size not in font_sizes:
                        font_sizes[size] = []
                    font_sizes[size].append((text, page_num))

    top_sizes = sorted(font_sizes.keys(), reverse=True)
    heading_levels = map_font_sizes_to_levels(top_sizes)

    # Title = first H1 on page 1
    if top_sizes:
        for text, page in font_sizes[top_sizes[0]]:
            if page == 1:
                title = text
                break

    for size, items in font_sizes.items():
        if size in heading_levels:
            for text, page in items:
                if text == title or not is_potential_heading(text):
                    continue
                outline.append({
                    "level": heading_levels[size],
                    "text": text,
                    "page": page
                })

    return {
        "title": title,
        "outline": sorted(outline, key=lambda x: x["page"])
    }
