import os
from dotenv import load_dotenv
from groq import Groq

from Backend.Agents.prompt import (
    REASONING_SYSTEM_PROMPT,
    NO_CONTEXT_RESPONSE
)

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)


class ReasoningAgent:
    """
    Reasoning Agent:
    - Generates final answer from retrieved context.
    - Applies output guardrails.
    """

    def __init__(self):
        self.model = "openai/gpt-oss-120b"

        self.unsafe_output_phrases = [
            "you should take",
            "i recommend taking",
            "start taking",
            "stop taking",
            "increase the dose",
            "decrease the dose",
            "you have",
            "you are diagnosed"
        ]

    def build_prompt(self, question: str, context: str) -> str:
        return f"""
{REASONING_SYSTEM_PROMPT}

Context:
{context}

User Question:
{question}

Answer:
"""

    def output_guardrail(self, answer: str) -> str:
        if not answer:
            return NO_CONTEXT_RESPONSE

        lower_answer = answer.lower()

        for phrase in self.unsafe_output_phrases:
            if phrase in lower_answer:
                return (
                    "Sorry, I cannot provide diagnosis, prescription, or treatment advice. "
                    "I can only explain what is written in the uploaded document."
                )

        return answer

    def run(self, question: str, context: str) -> dict:
        if not context or context.strip() == "":
            return {
                "answer": NO_CONTEXT_RESPONSE,
                "guardrail_passed": True,
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0
            }

        prompt = self.build_prompt(question, context)

        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.1
        )

        raw_answer = response.choices[0].message.content
        safe_answer = self.output_guardrail(raw_answer)

         # Token usage
        usage = getattr(response, "usage", None) #Get the value of this attribute from the object. If it doesn't exist, return the default value

        prompt_tokens = 0
        completion_tokens = 0
        total_tokens = 0

        if usage:
            prompt_tokens = getattr(usage, "prompt_tokens", 0)
            completion_tokens = getattr(usage, "completion_tokens", 0)
            total_tokens = getattr(usage, "total_tokens", 0)

        return {
            "answer": safe_answer,
            "guardrail_passed": safe_answer == raw_answer,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": total_tokens
        }


reasoning_agent = ReasoningAgent()