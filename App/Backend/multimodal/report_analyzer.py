import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def analyze_medical_text(ocr_text: str = "", vision_text: str = "") -> str:
    prompt = f"""
You are a safe medical document summarizer.

Use only the OCR text and vision analysis provided below.

STRICT RULES:
1. Do not diagnose.
2. Do not prescribe medicine.
3. Do not create your own recommendations.
4. Only explain what is written or visible in the uploaded document/image.
5. If medicine, dosage, frequency, findings, or impression is missing, say "Not clearly mentioned".
6. Recommendations must only be doctor-written recommendations from the document.
7. Do not add lifestyle advice unless it is written in the document.

OCR TEXT:
{ocr_text}

VISION ANALYSIS:
{vision_text}

Generate output:

Prescription / Report Summary:
- Document type:
- Patient name:
- Key details:

Medicines:
- Medicine:
- Dosage:
- Frequency:

Lab / X-Ray / Image Observations:
-

Doctor-written Recommendations:
-

Safety Note:
This summary is based only on the uploaded document/image.
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.1
    )

    return response.choices[0].message.content