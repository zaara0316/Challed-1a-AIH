import unicodedata

def detect_script(text):
    scripts = set()
    for char in text:
        try:
            name = unicodedata.name(char)
            if "DEVANAGARI" in name:
                scripts.add("Hindi")
            elif "CJK" in name or "HIRAGANA" in name or "KATAKANA" in name:
                scripts.add("Japanese")
            elif "HANGUL" in name:
                scripts.add("Korean")
            elif "ARABIC" in name:
                scripts.add("Arabic")
            elif "CYRILLIC" in name:
                scripts.add("Cyrillic")
            elif "HEBREW" in name:
                scripts.add("Hebrew")
            elif "THAI" in name:
                scripts.add("Thai")
            elif "LATIN" in name:
                scripts.add("Latin")
        except:
            continue
    return list(scripts)[0] if scripts else "Unknown"
