import os
from langchain_core.documents import Document
from Backend.multimodal.ocr import extract_text
from Backend.multimodal.image_processor import analyze_image_with_vision
from Backend.multimodal.report_analyzer import analyze_medical_text


class MultiModalAgent:
    """
    Multi Modal Agent:
    - Handles image files.
    - Runs OCR.
    - Runs Vision LLM.
    - Creates safe medical summary.
    - Converts image result into LangChain Document.
    """

    def is_image_file(self, file_path: str) -> bool:
        ext = os.path.splitext(file_path)[1].lower()
        return ext in [".png", ".jpg", ".jpeg"]

    def run(self, file_path: str) -> list[Document]:
        file_name = os.path.basename(file_path)

        if not self.is_image_file(file_path):
            raise ValueError("MultiModalAgent only supports image files.")

        ocr_text = extract_text(file_path)
        vision_text = analyze_image_with_vision(file_path)

        medical_summary = analyze_medical_text(
            ocr_text=ocr_text,
            vision_text=vision_text
        )

        final_text = f"""
OCR TEXT:
{ocr_text}

VISION ANALYSIS:
{vision_text}

MEDICAL SUMMARY:
{medical_summary}
"""

        txt_path = os.path.splitext(file_path)[0] + ".txt"

        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(final_text)

        docs = [
            Document(
                page_content=final_text,
                metadata={
                    "source": file_name,
                    "type": "medical_image"
                }
            )
        ]

        return docs


multi_modal_agent = MultiModalAgent()