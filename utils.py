import re
import json
import os

def clean_text(text):
    return re.sub(r"\s+", " ", text.strip())

def is_potential_heading(text):
    return len(text) > 3 and len(text.split()) > 1 and not text.strip().isdigit()

def map_font_sizes_to_levels(top_sizes):
    heading_levels = {}
    if len(top_sizes) > 0:
        heading_levels[top_sizes[0]] = "H1"
    if len(top_sizes) > 1:
        heading_levels[top_sizes[1]] = "H2"
    if len(top_sizes) > 2:
        heading_levels[top_sizes[2]] = "H3"
    return heading_levels

def save_json(data, output_dir, filename):
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, filename.replace(".pdf", ".json"))
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
