from Backend.MCP.tools import (
    Search_patients,
    Get_patient_history,
    Get_lab_results,
    Get_payment_summary
)


class McpAgent:
    """
    MCP Agent:
    - Handles PostgreSQL database questions.
    - Uses existing MCP tools.
    """

    def extract_patient_id(self, question: str):
        numbers = "".join(filter(str.isdigit, question))
        if numbers == "":
            return None
        return int(numbers)

    def format_records(self, records):
        if not records:
            return "No records found in database."

        answer = ""

        for index, record in enumerate(records, start=1):
            answer += f"Record {index}:\n"

            for key, value in record.items():
                answer += f"{key}: {value}\n"

            answer += "\n"

        return answer.strip()

    def run(self, question: str) -> dict:
        q = question.lower()

        if ("search patient" in q) or ("find patient" in q):
            name = (
                question.lower()
                .replace("search patient", "")
                .replace("find patient", "")
                .strip()
            )

            records = Search_patients(name)

            return {
                "answer": self.format_records(records),
                "sources": ["PostgreSQL Database"],
                "route": "mcp"
            }

        if ("patient history" in q) or ("medical history" in q):
            patient_id = self.extract_patient_id(question)

            if patient_id is None:
                return {
                    "answer": "Please provide patient_id. Example: get patient history 1",
                    "sources": ["PostgreSQL Database"],
                    "route": "mcp"
                }

            records = Get_patient_history(patient_id)

            return {
                "answer": self.format_records(records),
                "sources": ["PostgreSQL Database"],
                "route": "mcp"
            }

        if ("lab result" in q) or ("lab results" in q) or ("test result" in q):
            patient_id = self.extract_patient_id(question)

            if patient_id is None:
                return {
                    "answer": "Please provide patient_id. Example: get lab results 1",
                    "sources": ["PostgreSQL Database"],
                    "route": "mcp"
                }

            records = Get_lab_results(patient_id)

            return {
                "answer": self.format_records(records),
                "sources": ["PostgreSQL Database"],
                "route": "mcp"
            }

        if (
            "payment summary" in q
            or "billing summary" in q
            or "bill summary" in q
        ):
            patient_id = self.extract_patient_id(question)

            if patient_id is None:
                return {
                    "answer": "Please provide patient_id. Example: get payment summary 1",
                    "sources": ["PostgreSQL Database"],
                    "route": "mcp"
                }

            records = Get_payment_summary(patient_id)

            return {
                "answer": self.format_records(records),
                "sources": ["PostgreSQL Database"],
                "route": "mcp"
            }

        return {
            "answer": "Unsupported database question.",
            "sources": ["PostgreSQL Database"],
            "route": "mcp"
        }


mcp_agent = McpAgent()