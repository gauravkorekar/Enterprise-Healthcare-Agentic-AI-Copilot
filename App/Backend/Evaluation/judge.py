import json
import os

from dotenv import load_dotenv
from groq import Groq

from Backend.Evaluation.prompts import EVALUATION_PROMPT

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


class Judge:

    def clean_json_response(self, text):
        text = text.strip()
        text = text.replace("```json", "")
        text = text.replace("```", "")
        text = text.strip()

        start = text.find("{")
        end = text.rfind("}") + 1

        if start != -1 and end != -1:
            text = text[start:end]

        return text

    def evaluate(self, question, context, answer):
        prompt = EVALUATION_PROMPT.format(
            question=question,
            context=context,
            answer=answer
        )

        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0
        )

        try:
            response_text = response.choices[0].message.content
            cleaned_text = self.clean_json_response(response_text)

            return json.loads(cleaned_text)

        except Exception as e:
            print("Evaluation failed:", e)

            return {
                "relevance": 0,
                "groundedness": 0,
                "completeness": 0,
                "remarks": "Evaluation Failed"
            }


judge = Judge()