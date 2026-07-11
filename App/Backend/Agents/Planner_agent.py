from Backend.Agents.prompt import BLOCKED_RESPONSE

class PlannerAgent:
    """
    Planner Agent:
    - Applies input guardrails.
    - Decides whether question should go to:
      1. MCP database tools
      2. RAG document retrieval
      3. Blocked response
    """

    def __init__(self):
        self.blocked_keywords = [
            "what medicine should i take",
            "diagnose me",
            "treatment for",
            "cure for",
            "emergency",
            "should i stop medicine",
            "should i take",
            "medical advice"
        ]

        self.mcp_keywords = [
            "search patient",
            "find patient",
            "patient history",
            "medical history",
            "lab result",
            "lab results",
            "test result",
            "payment summary",
            "billing summary",
            "bill summary"
        ]

    def validate_input(self, question: str) -> dict:
        if not question or question.strip() == "":
            return {
                "is_valid": False,
                "route": "blocked",
                "reason": "Empty question",
                "answer": "Please enter a valid question."
            }

        q = question.lower().strip()

        for keyword in self.blocked_keywords:
            if keyword in q:
                return {
                    "is_valid": False,
                    "route": "blocked",
                    "reason": f"Blocked unsafe keyword: {keyword}",
                    "answer": BLOCKED_RESPONSE
                }

        return {
            "is_valid": True,
            "route": None,
            "reason": "Input passed guardrails",
            "answer": None
        }

    def detect_route(self, question: str) -> str:
        q = question.lower().strip()

        for keyword in self.mcp_keywords:
            if keyword in q:
                return "mcp"

        return "rag"           #If question is not database-related, it goes to uploaded documents.

    def run(self, question: str) -> dict:
        validation = self.validate_input(question)

        if not validation["is_valid"]:
            return validation

        route = self.detect_route(question)

        return {
            "is_valid": True,
            "route": route,
            "reason": f"Question routed to {route}",
            "answer": None
        }


planner_agent = PlannerAgent()
#This creates one reusable Planner Agent object. So other files can import it:
