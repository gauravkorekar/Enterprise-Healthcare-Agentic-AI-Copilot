EVALUATION_PROMPT = """
You are an evaluation agent.

Evaluate the answer using these metrics:
1. Relevance
2. Groundedness
3. Completeness

Return ONLY valid JSON.
Do not use markdown.
Do not use ```json.

JSON format:
{{
    "relevance": 10,
    "groundedness": 10,
    "completeness": 10,
    "remarks": "Answer is relevant and grounded."
}}

Question:
{question}

Context:
{context}

Answer:
{answer}
"""