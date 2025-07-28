import re

def is_heading(text):
    text = text.strip()

    if len(text.split()) < 2:
        return False

    if sum(c.isalpha() for c in text) < 5:
        return False

    if text.lower().startswith("rfp:") and len(text) > 30:
        return False

    repeated_numbers = re.findall(r"(\d+)(?:\s+\1){2,}", text)
    if repeated_numbers:
        return False

    return bool(re.match(r"^[\w\s\d,.\-():]+$", text)) and len(text.split()) <= 20

def merge_multiline_headings(text_blocks, line_gap_threshold=1.5):
    merged = []
    buffer = []
    last_size = None

    for text, size in text_blocks:
        if not buffer:
            buffer.append((text, size))
            last_size = size
        elif abs(size - last_size) <= line_gap_threshold:
            buffer.append((text, size))
        else:
            combined_text = " ".join([t for t, _ in buffer])
            merged.append((combined_text.strip(), last_size))
            buffer = [(text, size)]
            last_size = size

    if buffer:
        combined_text = " ".join([t for t, _ in buffer])
        merged.append((combined_text.strip(), last_size))

    return merged
