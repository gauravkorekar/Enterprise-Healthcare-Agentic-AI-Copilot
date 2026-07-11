import easyocr

reader = easyocr.Reader(["en"], gpu=False)

def extract_text(image_path: str) -> str:
    result = reader.readtext(image_path, detail=0)
    return " ".join(result).strip()