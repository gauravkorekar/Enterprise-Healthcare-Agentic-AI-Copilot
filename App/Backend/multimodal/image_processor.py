import os
import base64
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def encode_image(image_path: str) -> str:
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def analyze_image_with_vision(image_path: str) -> str:
    image_base64 = encode_image(image_path)

    prompt = """
You are a safe medical image understanding assistant.

Analyze the uploaded medical image, prescription, lab report, X-ray report, or scanned document.

Rules:
1. Do not diagnose.
2. Do not prescribe medicine.
3. Do not create new medical recommendations.
4. Only describe what is visible in the uploaded image.
5. If it is a prescription, identify medicines, dosage, and frequency if visible.
6. If it is a lab/X-ray report, identify visible findings/impression only if written or clearly visible.
7. If the actual X-ray image is shown, describe only visible visual features in simple non-diagnostic language.
8. If anything is unclear, say "Not clearly visible".
"""

    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_base64}"
                        }
                    }
                ]
            }
        ],
        temperature=0.1,
        max_tokens=500
    )

    return response.choices[0].message.content