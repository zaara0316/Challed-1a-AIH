from collections import defaultdict

def extract_outline(doc):
    font_sizes = defaultdict(list)
    outline = []
    title = ""

    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            for line in block.get("lines", []):
                for span in line["spans"]:
                    text = span["text"].strip()
                    if text:
                        size = round(span["size"], 1)
                        font_sizes[size].append((text, page_num))

    # Get top 3 largest font sizes
    top_sizes = sorted(font_sizes.keys(), reverse=True)[:3]
    heading_levels = {
        top_sizes[0]: "H1" if len(top_sizes) > 0 else "",
        top_sizes[1]: "H2" if len(top_sizes) > 1 else "",
        top_sizes[2]: "H3" if len(top_sizes) > 2 else "",
    }

    # Use first H1 heading on page 1 as title
    if top_sizes:
        for text, page in font_sizes[top_sizes[0]]:
            if page == 1:
                title = text
                break

    for size, items in font_sizes.items():
        if size in heading_levels:
            level = heading_levels[size]
            outline.extend(
                {"level": level, "text": text, "page": page}
                for text, page in items if text != title
            )

    return {
        "title": title,
        "outline": sorted(outline, key=lambda x: x["page"])
    }
