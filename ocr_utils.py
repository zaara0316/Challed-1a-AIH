import pytesseract
from pdf2image import convert_from_bytes

def ocr_page_as_text(doc, page_index, lang="hin+eng+jpn"):
    pix = doc[page_index].get_pixmap(dpi=200)
    img_bytes = pix.tobytes("png")
    try:
        return pytesseract.image_to_string(img_bytes, lang=lang).strip()
    except Exception as e:
        print(f"OCR failed on page {page_index}: {e}")
        return ""
