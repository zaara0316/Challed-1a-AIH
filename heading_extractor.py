def extract_outline(doc):
    font_sizes = {}
    outline = []
    title = ""
    
    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            for line in block.get("lines", []):
                for span in line["spans"]:
                    text = span["text"].strip()
                    if not text: continue
                    size = round(span["size"], 1)
                    if size not in font_sizes:
                        font_sizes[size] = []
                    font_sizes[size].append((text, page_num))
    
    # Detect top 3 sizes
    top_sizes = sorted(font_sizes.keys(), reverse=True)[:3]
    heading_levels = {top_sizes[0]: "H1", top_sizes[1]: "H2", top_sizes[2]: "H3"}

    # First H1 candidate on page 1 becomes title
    for text, page in font_sizes[top_sizes[0]]:
        if page == 1:
            title = text
            break

    for size, items in font_sizes.items():
        if size in heading_levels:
            for text, page in items:
                if text == title:
                    continue
                outline.append({
                    "level": heading_levels[size],
                    "text": text,
                    "page": page
                })

    return {"title": title, "outline": sorted(outline, key=lambda x: x["page"])}
